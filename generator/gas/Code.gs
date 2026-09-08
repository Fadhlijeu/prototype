/**
 * ==============================================================================
 * Prototype Autonomous Generator — Google Apps Script (GAS) Cloud Gateway
 * ==============================================================================
 * 
 * ARSITEKTUR & KEAMANAN:
 * 1. JANGAN PERNAH menuliskan API key atau kata sandi langsung di file kode ini.
 * 2. Simpan semua kredensial di:
 *    Apps Script Editor > Project Settings (Ikon Gear) > Script Properties.
 *
 * SCRIPT PROPERTIES YANG DIDUKUNG:
 * - ADMIN_PASSKEY         : Kata sandi rahasia untuk memproteksi Generator Lab (Mencegah publik memicu bot)
 * - GEMINI_API_KEY        : Google AI Studio API Key (untuk model gemini-3.*)
 * - TOKENROUTER_API_KEY   : TokenRouter API Key (https://api.tokenrouter.com/v1)
 * - ROUTER_API_KEY        : 9Router / OpenAI Gateway Token (jika cloud)
 * - GITHUB_REPO_TOKEN     : GitHub Personal Access Token (PAT) dengan scope 'repo'
 * - GITHUB_REPO           : "Fadhlijeu/prototype"
 * ==============================================================================
 */

/**
 * Mengambil secret secara aman dari Script Properties
 */
function getSecret(key, defaultValue) {
  var props = PropertiesService.getScriptProperties();
  var val = props.getProperty(key);
  if (!val) {
    if (defaultValue !== undefined) return defaultValue;
    throw new Error("Script Property '" + key + "' belum diset di Project Settings.");
  }
  return val;
}

/**
 * Webhook Entrypoint (doPost)
 * Menerima request HTTP POST dari Webhook eksternal, cURL, atau form remote.
 */
function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }

    var adminPasskey = "";
    try {
      adminPasskey = getSecret("ADMIN_PASSKEY", "");
    } catch(err) {
      adminPasskey = "";
    }

    // Aksi 1: Verifikasi Auth / Passkey dari UI Generator Lab
    if (data.action === "verify_passkey" || data.action === "verify_auth") {
      if (!adminPasskey) {
        return ContentService.createTextOutput(JSON.stringify({
          status: "AUTHENTICATED",
          ok: true,
          unconfigured: true,
          message: "Passkey diterima. (Catatan: ADMIN_PASSKEY belum diset di Script Properties)."
        })).setMimeType(ContentService.MimeType.JSON);
      }

      if (data.passkey === adminPasskey) {
        return ContentService.createTextOutput(JSON.stringify({
          status: "AUTHENTICATED",
          ok: true,
          message: "Autentikasi berhasil. Akses cloud terbuka."
        })).setMimeType(ContentService.MimeType.JSON);
      } else {
        return ContentService.createTextOutput(JSON.stringify({
          status: "UNAUTHORIZED",
          ok: false,
          error: "Passkey salah. Akses ditolak."
        })).setMimeType(ContentService.MimeType.JSON);
      }
    }

    // Aksi 2: Eksekusi Generator / Dispatch — Wajib validasi Passkey jika ADMIN_PASSKEY diset
    if (adminPasskey && data.passkey !== adminPasskey) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "UNAUTHORIZED",
        ok: false,
        error: "Akses ditolak: Passkey salah atau tidak valid."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Aksi 3: Persetujuan / Curation Approval dari Web UI
    if (data.action === "approve_item" && data.item_id) {
      var appRes = dispatchApproveToGitHub(data.item_id);
      return ContentService.createTextOutput(JSON.stringify({
        status: "APPROVED_DISPATCHED",
        ok: true,
        message: "Perintah persetujuan komponen diteruskan ke GitHub Actions",
        dispatch: appRes
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Aksi 4: Penolakan / Curation Rejection dari Web UI
    if (data.action === "reject_item" && data.item_id) {
      var rejRes = dispatchRejectToGitHub(data.item_id);
      return ContentService.createTextOutput(JSON.stringify({
        status: "REJECTED_DISPATCHED",
        ok: true,
        message: "Perintah penolakan komponen diteruskan ke GitHub Actions",
        dispatch: rejRes
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var prompt = data.prompt || "Aurora Glass Floating Input with Glow";
    var category = data.category || "other";
    var directive = data.directive || "Explore new creative dark glass variations adhering to design tokens";
    var mode = data.mode || "dispatch"; // 'dispatch' (ke GitHub Actions) atau 'direct' (generate langsung di GAS)

    if (mode === "direct") {
      var generatedOutput = generateWithGeminiDirect(prompt);
      return ContentService.createTextOutput(JSON.stringify({
        status: "GENERATED",
        ok: true,
        prompt: prompt,
        output_snippet: generatedOutput.substring(0, 300) + "..."
      })).setMimeType(ContentService.MimeType.JSON);
    } else {
      var dispatchResult = dispatchToGitHub(prompt, category, directive);
      return ContentService.createTextOutput(JSON.stringify({
        status: "QUEUED",
        ok: true,
        message: "Tugas berhasil diteruskan ke antrean GitHub Actions",
        dispatch: dispatchResult
      })).setMimeType(ContentService.MimeType.JSON);
    }

  } catch (err) {
    Logger.log("Error in doPost: " + err.toString());
    return ContentService.createTextOutput(JSON.stringify({
      status: "ERROR",
      ok: false,
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Webhook Test Endpoint (doGet)
 * Menampilkan status ketersediaan gateway saat diakses via browser.
 */
function doGet() {
  var hasPasskey = false;
  try {
    hasPasskey = !!getSecret("ADMIN_PASSKEY", "");
  } catch(e) {}

  return ContentService.createTextOutput(JSON.stringify({
    status: "ONLINE",
    service: "Prototype Autonomous Generator Gateway (GAS)",
    timestamp: new Date().toISOString(),
    passkey_protection_active: hasPasskey,
    supported_providers: ["gemini", "9router", "tokenrouter"]
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * METODE 1: Memicu GitHub Actions Runner via repository_dispatch
 */
function dispatchToGitHub(prompt, category, directive) {
  var githubToken = getSecret("GITHUB_REPO_TOKEN");
  var repo = getSecret("GITHUB_REPO", "Fadhlijeu/prototype");
  
  var url = "https://api.github.com/repos/" + repo + "/dispatches";
  var payload = {
    event_type: "generate_task",
    client_payload: {
      prompt: prompt,
      category: category,
      directive: directive,
      source: "google_apps_script_cloud_trigger",
      timestamp: new Date().toISOString()
    }
  };

  var options = {
    method: "post",
    headers: {
      "Authorization": "Bearer " + githubToken,
      "Accept": "application/vnd.github.v3+json",
      "Content-Type": "application/json"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var code = response.getResponseCode();
  return { success: code >= 200 && code < 300, statusCode: code };
}

/**
 * Memicu persetujuan komponen ke GitHub Actions
 */
function dispatchApproveToGitHub(itemId) {
  var githubToken = getSecret("GITHUB_REPO_TOKEN");
  var repo = getSecret("GITHUB_REPO", "Fadhlijeu/prototype");
  
  var url = "https://api.github.com/repos/" + repo + "/dispatches";
  var payload = {
    event_type: "approve_task",
    client_payload: {
      action: "approve",
      item_id: itemId,
      timestamp: new Date().toISOString()
    }
  };

  var options = {
    method: "post",
    headers: {
      "Authorization": "Bearer " + githubToken,
      "Accept": "application/vnd.github.v3+json",
      "Content-Type": "application/json"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var code = response.getResponseCode();
  return { success: code >= 200 && code < 300, statusCode: code };
}

/**
 * Memicu penolakan komponen ke GitHub Actions
 */
function dispatchRejectToGitHub(itemId) {
  var githubToken = getSecret("GITHUB_REPO_TOKEN");
  var repo = getSecret("GITHUB_REPO", "Fadhlijeu/prototype");
  
  var url = "https://api.github.com/repos/" + repo + "/dispatches";
  var payload = {
    event_type: "reject_task",
    client_payload: {
      action: "reject",
      item_id: itemId,
      timestamp: new Date().toISOString()
    }
  };

  var options = {
    method: "post",
    headers: {
      "Authorization": "Bearer " + githubToken,
      "Accept": "application/vnd.github.v3+json",
      "Content-Type": "application/json"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var code = response.getResponseCode();
  return { success: code >= 200 && code < 300, statusCode: code };
}

/**
 * METODE 2: Direct AI Call di Serverless Google (Gemini API)
 */
function generateWithGeminiDirect(prompt) {
  var apiKey = getSecret("GEMINI_API_KEY");
  var model = "gemini-3.5-flash-lite";
  var url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent?key=" + apiKey;

  var systemInstruction = "You are the UI Component Architect for this design system. Generate complete single-file dark glassmorphism component HTML referencing ../css.css tokens and Lucide icons.";
  
  var payload = {
    systemInstruction: { parts: [{ text: systemInstruction }] },
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.7, maxOutputTokens: 4096 }
  };

  var options = {
    method: "post",
    headers: { "Content-Type": "application/json" },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var json = JSON.parse(response.getContentText());
  return json.candidates[0].content.parts[0].text;
}

/**
 * Trigger Otomatis Berulang (Cron Trigger)
 * Frekuensi bisa diatur di Triggers (Ikon Jam):
 * - Minutes timer: Every 5 minutes, Every 10 minutes, Every 15 minutes, Every hour
 *
 * Tiap kali jalan, fungsi ini men-dispatch variasi batch otonom ke GitHub Actions.
 */
function autonomousCronTrigger() {
  Logger.log("Menjalankan siklus otonom cloud Prototype...");
  
  // Koleksi seed kaya variasi: Single Molecules, Compound Organisms, Scenery, Dashboards, & Experimental Other
  var seedPool = [
    "Glass scenery composite workstation viewport with weather node, server metrics and quick action dock",
    "Obsidian glass telemetry command center dashboard with mini sparkline charts and live status matrix",
    "Liquid frosted breadcrumb navigation with spring pill indicators",
    "Floating glass telemetry dial gauge with specular illumination",
    "Aurora glass interactive slider with magnetic haptic tick marks",
    "Specular frosted floating action button with expandable speed dial",
    "Experimental obsidian glass circular command wheel with radial touch hotspots",
    "Aurora ambient gradient notification banner with refractive glass blur",
    "Glass password strength meter with animated glowing segments",
    "Cyberpunk dark glass HUD scenery with floating telemetry widgets",
    "Holographic glass timeline node with reactive particle trail",
    "Obsidian glass segmented audio visualizer bar with live meter",
    "Liquid refraction multi-tab switcher with frosted specular pill",
    "Dark glass floating telemetry node with dual ring dial and live latency"
  ];
  
  // Acak dan kirim Batch (misal 2 komponen sekaligus per trigger)
  var BATCH_COUNT = 2;
  var shuffled = seedPool.sort(function() { return 0.5 - Math.random(); });
  
  for (var i = 0; i < Math.min(BATCH_COUNT, shuffled.length); i++) {
    var prompt = shuffled[i];
    Logger.log("Dispatching batch item #" + (i + 1) + ": " + prompt);
    dispatchToGitHub(prompt, "other", "Explore diverse novel glass paradigms and scenery");
    Utilities.sleep(1500); // jeda 1.5 detik antar dispatch
  }
}
