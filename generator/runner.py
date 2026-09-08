import os
import sys
import time
import argparse
import json

from .engine.decision_engine import DecisionEngine
from .engine.model_router import ModelRouter
from .engine.generator_engine import GeneratorEngine
from .engine.decompiler import Decompiler
from .engine.validator import Validator
from .engine.deduplicator import Deduplicator
from .engine.queue_manager import QueueManager
from .curation.curator import Curator

def build_pipeline(root_dir: str = None):
    root_dir = root_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    queue = QueueManager(os.path.join(root_dir, "generator", "queue"))
    dedup = Deduplicator(os.path.join(root_dir, "ui", "components", "glass"))
    pending_slugs = [it.get("slug") for it in queue.get_pending_items() if it.get("slug")]
    all_known_slugs = list(set(dedup.get_existing_slugs() + pending_slugs))
    decision = DecisionEngine(all_known_slugs)
    router = ModelRouter(os.path.join(root_dir, "generator", "config", "models.json"))
    engine = GeneratorEngine(root_dir, router)
    decompiler = Decompiler()
    validator = Validator()
    curator = Curator(root_dir, queue)
    return {
        "root_dir": root_dir,
        "queue": queue,
        "dedup": dedup,
        "decision": decision,
        "router": router,
        "engine": engine,
        "decompiler": decompiler,
        "validator": validator,
        "curator": curator
    }

def run_single_generation(prompt: str, pipeline: dict, auto_approve: bool = False, force_provider: str = None):
    print(f"\n[1/5] Decision Layer: Analyzing prompt -> '{prompt}'...")
    spec = pipeline["decision"].classify_intent(prompt)
    print(f"      Identified: Title='{spec['title']}', Category='{spec['category']}', Variation='{spec['variation']}'")

    # Deduplication Check
    is_dup, sim, dup_matched = pipeline["dedup"].check_similarity(spec["slug"], spec["title"])
    if is_dup:
        print(f"      [WARNING] Detected high similarity ({sim*100:.1f}%) with existing '{dup_matched}'. Adjusting slug...")
        spec["slug"] = f"{spec['slug']}-alt-{int(time.time()) % 1000}"

    print(f"\n[2/5] Model Router & Generation Engine: Invoking active model cascade...")
    if force_provider == "mock":
        # Force mock provider
        raw_html = pipeline["router"]._call_mock("system", prompt)
        router_meta = {"provider": "mock", "model": "mock-glass-generator-v1", "status": "forced_mock"}
    else:
        raw_html, router_meta = pipeline["engine"].generate(spec, pipeline["dedup"].get_existing_names())

    print(f"      Generated {len(raw_html)} bytes via {router_meta.get('provider')}:{router_meta.get('model')}")

    print(f"\n[3/5] Decompiler: Extracting modular files & manifest...")
    decompiled = pipeline["decompiler"].decompile(raw_html, spec)
    print(f"      Decompiled into: {decompiled['standalone_file']}, index.html, index.css, index.js, manifest.json")

    print(f"\n[4/5] Validator: Running quality and token compliance checks...")
    val = pipeline["validator"].validate(decompiled)
    print(f"      Validation: Valid={val['valid']} | Score={val['score']}/100")
    if val["warnings"]:
        for w in val["warnings"]:
            print(f"      [WARN] {w}")
    if val["errors"]:
        for e in val["errors"]:
            print(f"      [ERROR] {e}")

    print(f"\n[5/5] Queue Manager: Transitioning to review lifecycle...")
    if pipeline["queue"].is_queue_full():
        print("      [ALERT] Pending review queue is FULL (>= 100 items). Generation paused.")
        return None

    item_id = pipeline["queue"].enqueue_pending(decompiled, val, router_meta)
    print(f"      Successfully enqueued to: generator/queue/pending/{item_id}")

    # Export web manifest for Generator Lab UI review
    try:
        manifest_out = os.path.join(pipeline["root_dir"], "projects", "generator-lab", "queue.json")
        pipeline["queue"].export_web_manifest(manifest_out)
        print(f"      Exported web manifest to: projects/generator-lab/queue.json")
    except Exception as ex:
        print(f"      [WARN] Could not export web manifest: {ex}")

    if auto_approve:
        print("\n[AUTO-APPROVE] Approving and deploying component to core design system...")
        deploy_res = pipeline["curator"].approve_and_deploy(item_id, auto_rebuild=True)
        if deploy_res.get("success"):
            print(f"      Deployed to: {deploy_res.get('deployed_to')}")
            print(f"      Rebuild status: OK")
            # Update web manifest after approval
            try:
                pipeline["queue"].export_web_manifest(manifest_out)
            except Exception:
                pass

    return item_id

def main():
    parser = argparse.ArgumentParser(description="Prototype Autonomous UI Generator & Curation Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate a single UI component")
    gen_parser.add_argument("--prompt", type=str, default="Aurora Glass Segmented Stepper", help="Component prompt instruction")
    gen_parser.add_argument("--provider", type=str, choices=["gemini", "9router", "mock"], help="Force specific provider")
    gen_parser.add_argument("--auto-approve", action="store_true", help="Automatically approve and install to design system")

    # Command: run (autonomous loop)
    run_parser = subparsers.add_parser("run", help="Run continuous autonomous generator loop")
    run_parser.add_argument("--continuous", action="store_true", help="Keep running indefinitely until queue full or stopped")
    run_parser.add_argument("--max-iterations", type=int, default=3, help="Max iterations before pausing")
    run_parser.add_argument("--delay", type=int, default=2, help="Seconds delay between cycles")
    run_parser.add_argument("--provider", type=str, choices=["gemini", "9router", "mock"], default="mock", help="Provider to use")

    # Command: curate
    cur_parser = subparsers.add_parser("curate", help="Manage review queue and curation decisions")
    cur_parser.add_argument("--list", action="store_true", help="List all pending components")
    cur_parser.add_argument("--approve", type=str, metavar="ITEM_ID", help="Approve and deploy component")
    cur_parser.add_argument("--reject", type=str, metavar="ITEM_ID", help="Reject and archive component")
    cur_parser.add_argument("--reason", type=str, default="Human rejection", help="Rejection rationale")
    cur_parser.add_argument("--stats", action="store_true", help="Display queue statistics")

    args = parser.parse_args()
    pipeline = build_pipeline()

    if args.command == "generate":
        run_single_generation(args.prompt, pipeline, auto_approve=args.auto_approve, force_provider=args.provider)

    elif args.command == "run":
        print("=== Autonomous Generator Loop Starting ===")
        seeds = [
            "Floating glass telemetry dial gauge with specular illumination",
            "Specular frosted breadcrumb navigation with spring pill indicators",
            "Obsidian glass segmented audio visualizer bar",
            "Aurora ambient gradient notification banner",
            "Glass interactive slider with magnetic haptic feedback"
        ]
        iterations = 0
        while True:
            if pipeline["queue"].is_queue_full():
                print("[ALERT] Pending queue reached capacity limit. Stopping autonomous loop.")
                break

            seed_prompt = seeds[iterations % len(seeds)]
            print(f"\n--- [Cycle #{iterations+1}] Autonomous Pulse: '{seed_prompt}' ---")
            run_single_generation(seed_prompt, pipeline, auto_approve=False, force_provider=args.provider)
            iterations += 1

            if not args.continuous and iterations >= args.max_iterations:
                print(f"\nReached max iterations ({args.max_iterations}). Pausing autonomous loop.")
                break

            time.sleep(args.delay)

    elif args.command == "curate":
        if args.stats or (not args.list and not args.approve and not args.reject):
            stats = pipeline["queue"].get_stats()
            print("\n=== Curation Queue Statistics ===")
            print(f"  Pending Review : {stats['pending']}")
            print(f"  Approved       : {stats['approved']}")
            print(f"  Rejected       : {stats['rejected']}")

        if args.list:
            items = pipeline["curator"].list_pending()
            print(f"\n=== Pending Review Items ({len(items)}) ===")
            if not items:
                print("  No pending items in queue.")
            for it in items:
                v = it.get("validation", {})
                print(f"- ID: {it.get('item_id')}")
                print(f"  Slug: {it.get('slug')} | Score: {v.get('score', 'N/A')}/100 | Provider: {it.get('router', {}).get('provider')}")
                print(f"  Created: {it.get('created_at')}")

        if args.approve:
            print(f"\nApproving item '{args.approve}'...")
            res = pipeline["curator"].approve_and_deploy(args.approve, auto_rebuild=True)
            if res.get("success"):
                print(f"[SUCCESS] Approved and deployed to: {res.get('deployed_to')}")
            else:
                print(f"[FAILED] {res.get('error')}")
            try:
                manifest_out = os.path.join(pipeline["root_dir"], "projects", "generator-lab", "queue.json")
                pipeline["queue"].export_web_manifest(manifest_out)
            except Exception:
                pass

        if args.reject:
            print(f"\nRejecting item '{args.reject}'...")
            res = pipeline["curator"].reject(args.reject, reason=args.reason)
            if res.get("success"):
                print(f"[SUCCESS] Item moved to rejected queue.")
            else:
                print(f"[FAILED] Could not reject item.")
            try:
                manifest_out = os.path.join(pipeline["root_dir"], "projects", "generator-lab", "queue.json")
                pipeline["queue"].export_web_manifest(manifest_out)
            except Exception:
                pass

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
