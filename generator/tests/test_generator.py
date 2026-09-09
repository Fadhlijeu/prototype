import os
import shutil
import tempfile
import unittest

from generator.engine.decision_engine import DecisionEngine
from generator.engine.model_router import ModelRouter
from generator.engine.generator_engine import GeneratorEngine
from generator.engine.decompiler import Decompiler
from generator.engine.validator import Validator
from generator.engine.deduplicator import Deduplicator
from generator.engine.queue_manager import QueueManager
from generator.curation.curator import Curator

class TestGeneratorPipeline(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.queue_dir = os.path.join(self.test_dir, "queue")
        self.queue_mgr = QueueManager(self.queue_dir)
        self.router = ModelRouter()
        self.decompiler = Decompiler()
        self.validator = Validator()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_decision_engine_classification(self):
        decision = DecisionEngine()
        spec = decision.classify_intent("buat input login glass animasi glowing")
        self.assertEqual(spec["family"], "glass")
        self.assertEqual(spec["theme"], "dark")
        self.assertEqual(spec["category"], "inputs")
        self.assertIn("glass", spec["slug"])
        self.assertIsInstance(spec["tags"], list)

    def test_model_router_fallback(self):
        # 1. In production (allow_mock=False), failure without API keys raises RuntimeError
        with self.assertRaises(RuntimeError):
            self.router.call_with_cascade("System instruction", "Create glass widget", allow_mock=False)

        # 2. When allow_mock=True or force_provider="mock", cascade resolves to mock
        output, meta = self.router.call_with_cascade("System instruction", "Create glass widget", allow_mock=True)
        self.assertIn("<html", output.lower())
        self.assertIn("mock", meta["provider"].lower())

    def test_variation_genome_generation(self):
        decision = DecisionEngine()
        spec = decision.classify_intent("desain slider presisi haptic")
        self.assertIn("genome", spec)
        genome = spec["genome"]
        self.assertIn("geometry", genome)
        self.assertIn("palette", genome)
        self.assertIn("interaction", genome)
        self.assertIn("novelty_target", genome)

    def test_decompiler_modularization(self):
        mock_html = """<!DOCTYPE html>
<html>
<head>
    <style>.glass-test { color: red; backdrop-filter: blur(8px); }</style>
</head>
<body>
    <div class="glass-test">Hello</div>
    <script id="component-manifest" type="application/json">
    {"title": "Test Component", "slug": "test-component", "category": "inputs"}
    </script>
    <script>console.log("Interactive!");</script>
</body>
</html>"""
        spec = {"slug": "test-component", "title": "Test Component"}
        res = self.decompiler.decompile(mock_html, spec)

        self.assertEqual(res["slug"], "test-component")
        self.assertIn("index_html", res)
        self.assertIn("index_css", res)
        self.assertIn("index_js", res)
        self.assertIn("backdrop-filter", res["index_css"])
        self.assertIn('console.log("Interactive!");', res["index_js"])

    def test_validator_compliance(self):
        valid_spec = {
            "standalone_content": '<!DOCTYPE html><html><body><button aria-label="Test">Btn</button></body></html>',
            "index_css": ".test { backdrop-filter: blur(12px); --glass-surface-1: rgba(255,255,255,0.05); }",
            "index_js": "document.addEventListener('DOMContentLoaded', () => {});"
        }
        res = self.validator.validate(valid_spec)
        self.assertTrue(res["valid"])
        self.assertGreaterEqual(res["score"], 60)

        # Test forbidden library rejection
        invalid_spec = {
            "standalone_content": '<!DOCTYPE html><html><head><link href="tailwindcss.css"></head><body>Bad</body></html>',
            "index_css": "body { margin: 0; }",
            "index_js": ""
        }
        inv_res = self.validator.validate(invalid_spec)
        self.assertFalse(inv_res["valid"])
        self.assertTrue(any("forbidden" in e.lower() for e in inv_res["errors"]))

    def test_deduplicator_similarity(self):
        dedup = Deduplicator()
        is_dup, score, matched = dedup.check_similarity("button-glass", "Glass Buttons Collection")
        # Should detect high similarity with existing button-glass
        self.assertTrue(is_dup)
        self.assertGreater(score, 0.7)

    def test_queue_lifecycle(self):
        decompiled = {
            "slug": "test-widget",
            "standalone_file": "test-widget.html",
            "standalone_content": "<html><body>Widget</body></html>",
            "index_html": "<html><body>Widget Demo</body></html>",
            "index_css": "/* css */",
            "index_js": "// js",
            "manifest_json": '{"title": "Test Widget"}'
        }
        val = {"valid": True, "score": 90, "errors": [], "warnings": []}
        router_meta = {"provider": "mock", "model": "mock-v1"}

        item_id = self.queue_mgr.enqueue_pending(decompiled, val, router_meta)
        self.assertTrue(os.path.exists(os.path.join(self.queue_dir, "pending", item_id)))

        items = self.queue_mgr.get_pending_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_id"], item_id)

        # Approve item
        approved_dir = self.queue_mgr.approve(item_id)
        self.assertTrue(os.path.exists(approved_dir))
        self.assertEqual(len(self.queue_mgr.get_pending_items()), 0)

        stats = self.queue_mgr.get_stats()
        self.assertEqual(stats["approved"], 1)
        self.assertEqual(stats["pending"], 0)

    def test_rejection_archiving_and_manifest_export(self):
        decompiled = {
            "slug": "test-rejected-widget",
            "standalone_file": "test-rejected-widget.html",
            "standalone_content": "<html><body>Bad Widget</body></html>",
            "index_html": "<html><body>Bad Widget Demo</body></html>",
            "index_css": "/* css */",
            "index_js": "// js",
            "manifest_json": '{"title": "Test Rejected Widget", "slug": "test-rejected-widget"}'
        }
        val = {"valid": True, "score": 75, "errors": [], "warnings": []}
        router_meta = {"provider": "mock", "model": "mock-v1"}

        item_id = self.queue_mgr.enqueue_pending(decompiled, val, router_meta)
        self.assertEqual(len(self.queue_mgr.get_pending_items()), 1)

        # Reject item
        rej_dir = self.queue_mgr.reject(item_id, reason="Too repetitive")
        self.assertTrue(os.path.isdir(rej_dir))
        self.assertTrue(os.path.exists(os.path.join(rej_dir, "rejection.json")))
        self.assertEqual(len(self.queue_mgr.get_pending_items()), 0)
        self.assertEqual(len(self.queue_mgr.get_rejected_items()), 1)

        # Test negative memory
        neg_sigs = self.queue_mgr.get_rejected_signatures()
        self.assertEqual(len(neg_sigs), 1)
        self.assertEqual(neg_sigs[0]["slug"], "test-rejected-widget")

        # Test export web manifest with all 3 states
        manifest_path = os.path.join(self.test_dir, "queue.json")
        self.queue_mgr.export_web_manifest(manifest_path)
        import json
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("pending", data)
        self.assertIn("approved", data)
        self.assertIn("rejected", data)
        self.assertIn("stats", data)
        self.assertEqual(len(data["rejected"]), 1)

if __name__ == "__main__":
    unittest.main()
