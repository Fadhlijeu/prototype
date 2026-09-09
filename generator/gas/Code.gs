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
 * CORS Preflight Handler (doOptions)
 * Menangani permintaan preflight OPTIONS dari browser secara elegan.
 */
function doOptions(e) {
  return ContentService.createTextOutput("")
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Verifikasi passkey secara aman dan toleran terhadap whitespace dan tipe data.
 */
function verifyPasskeyInternal(passkeyInput) {
  var adminPasskey = "";
  try {
    adminPasskey = getSecret("ADMIN_PASSKEY", "");
  } catch(err) {
    adminPasskey = "";
  }

  var cleanAdminPass = String(adminPasskey !== undefined && adminPasskey !== null ? adminPasskey : "").trim();
  var cleanPasskey = String(passkeyInput !== undefined && passkeyInput !== null ? passkeyInput : "").trim();

  // Jika ADMIN_PASSKEY belum diset di Script Properties: izinkan (setup/unconfigured mode)
  if (!cleanAdminPass) {
    return {
      status: "AUTHENTICATED",
      ok: true,
      unconfigured: true,
      message: "Passkey diterima. (Catatan: ADMIN_PASSKEY belum diset di Script Properties)."
    };
  }

  // Jika passkey cocok secara eksak (setelah trim)
  if (cleanPasskey === cleanAdminPass) {
    return {
      status: "AUTHENTICATED",
      ok: true,
      message: "Autentikasi berhasil. Akses cloud terbuka."
    };
  }

  // Jika passkey salah
  return {
    status: "UNAUTHORIZED",
    ok: false,
    error: "Passkey salah. Akses ditolak."
  };
}

/**
 * Ekstraksi payload dari berbagai format request (JSON string, URL-encoded, parameter)
 */
function extractPayload(e) {
  var data = {};
  if (!e) return data;

  if (e.postData && e.postData.contents) {
    var raw = e.postData.contents;
    try {
      data = JSON.parse(raw);
    } catch(err1) {
      try {
        data = JSON.parse(decodeURIComponent(raw));
      } catch(err2) {
        try {
          if (typeof raw === "string" && raw.indexOf("=") !== -1) {
            data = {};
            raw.split("&").forEach(function(pair) {
              var parts = pair.split("=");
              if (parts.length >= 2) {
                var k = decodeURIComponent(parts[0].replace(/\+/g, " "));
                var v = decodeURIComponent(parts.slice(1).join("=").replace(/\+/g, " "));
                data[k] = v;
              }
            });
          }
        } catch(err3) {
          data = {};
        }
      }
    }
  }

  if (e.parameter && typeof e.parameter === "object") {
    for (var key in e.parameter) {
      if (data[key] === undefined) {
        data[key] = e.parameter[key];
      }
    }
  }

  return data;
}

/**
 * Webhook Entrypoint (doPost)
 * Menerima request HTTP POST dari Webhook eksternal, cURL, atau form remote.
 * Mampu mem-parsing payload application/json maupun text/plain (CORS-safe).
 */
function doPost(e) {
  try {
    var data = extractPayload(e);

    // Aksi 1: Verifikasi Auth / Passkey dari UI Generator Lab
    if (data.action === "verify_passkey" || data.action === "verify_auth") {
      var authRes = verifyPasskeyInternal(data.passkey);
      return ContentService.createTextOutput(JSON.stringify(authRes))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Aksi 2: Validasi Passkey untuk seluruh operasi cloud generator & kurasi
    var authCheck = verifyPasskeyInternal(data.passkey);
    if (!authCheck.ok) {
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
 * Webhook Test Endpoint & GET verification (doGet)
 * Menampilkan status gateway atau memvalidasi passkey melalui parameter query string.
 */
function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : "";
  if (action === "verify_passkey" || action === "verify_auth") {
    var passkey = (e && e.parameter && e.parameter.passkey) ? e.parameter.passkey : "";
    var authResult = verifyPasskeyInternal(passkey);
    return ContentService.createTextOutput(JSON.stringify(authResult))
      .setMimeType(ContentService.MimeType.JSON);
  }

  var hasPasskey = false;
  try {
    hasPasskey = !!String(getSecret("ADMIN_PASSKEY", "")).trim();
  } catch(err) {}

  return ContentService.createTextOutput(JSON.stringify({
    status: "ONLINE",
    ok: true,
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
 * Menghasilkan instruksi otonom kreatif beragam (Category-Aware Creative Directives).
 * AI Web Engineer diarahkan untuk menghasilkan variasi bentuk, palet warna, dan mekanisme interaktif
 * yang berbeda di tiap kategori (sliders, telemetry, controls, navigation, buttons, scenery, dashboards, etc).
 */
function generateAutonomousPrompt(category) {
  var categoryDirectives = {
    "sliders": [
      "Ciptakan komponen Aurora Magnetic Precision Slider bertema Dark Glass. Rancang track presisi dengan magnetic tick marks haptic, numeric badge HUD, dan thumb slider bersinar biru elektrik (#60A5FA). Wajib interaktif dengan JavaScript.",
      "Desain Refraction Density Optical Scrubber untuk kontrol visual. Gunakan glass slider horizontal dengan nilai persentase live, efek liquid refraction, dan specular top border.",
      "Rancang Radial Arc Fader Slider dengan thumb melengkung interaktif, angka persentase di tengah, dan ambient purple-rose glow (#F472B6).",
      "Ciptakan Vertical Glass Equalizer Slider Strip dengan skala desibel numerik dan efek haptic dragging halus.",
      "Desain Bi-Directional Dual Balance Slider berkepala ganda dengan titik nol di tengah dan aksen neon cyan."
    ],
    "telemetry": [
      "Rancang komponen Neon Cyan & Emerald Live Telemetry Dial Gauge atau Audio Visualizer. Buat indikator visual gelombang/meter aktif dengan palet cyan (#22D3EE) dan emerald (#10B981) yang menyala di atas canvas obsidian gelap.",
      "Ciptakan Dual Arc Specular Latency Monitor dengan metrik live ping, status node mesh, dan animasi fluctuating graph mikro yang elegan.",
      "Desain Concentric Radar System Topology Meter dengan orbit status node berputar dan metrik throughput live.",
      "Ciptakan Hexagonal Hardware Stat Cluster dengan pembacaan suhu CPU, memory pressure, dan bus IO berlapis kaca frosted.",
      "Rancang Bioluminescent Audio Frequency Bar Chart dengan 12 batang spektrum suara teranimasi dan glow reaktif."
    ],
    "controls": [
      "Ciptakan Segmented Frosted Capsule Switch (border-radius: 9999px) dengan pilihan mode Eco / Balanced / Turbo. Tombol aktif berpindah dengan spring animation halus dan aksen warna mint green (#34D399).",
      "Rancang Tactile Obsidian Power Toggle dengan indikator glowing LED status dan efek glass click interaktif.",
      "Desain Rotary Multi-Step Selector Wheel dengan indikator klik sudut diskrit dan specular top rim highlight.",
      "Ciptakan Quad-State Glass Rocker Switch bergaya kontrol kokpit luar angkasa dengan haptic feedback visual.",
      "Rancang Floating Minimalist Pill Checkbox Matrix dengan animasi checkmark liquid dan glowing focus ring."
    ],
    "buttons": [
      "Desain Specular Action Speed Dial / Floating Action Button dengan expandable speed dial options, aksen hot pink / violet glow (#F472B6), dan spring elevation saat dihover.",
      "Ciptakan Micro-Elevation Action Trigger Group dengan tombol snapshot & deploy berlatar frosted glass specular.",
      "Rancang Prismatic Radial Launch Trigger dengan pulsing optic ring dan countdown confirmation state.",
      "Ciptakan Magnetic Split Button Pill dengan tombol aksi utama dan trigger menu dropdown terintegrasi.",
      "Desain Floating Crystal Pill FAB dengan transisi rotasi icon saat diklik dan expand ke status dock."
    ],
    "navigation": [
      "Rancang Frosted Capsule Dock Bar (border-radius: 9999px) dengan icon Lucide floating, pill indicator aktif berbahan liquid glass, dan transisi spring physics.",
      "Ciptakan Breadcrumb Stepper Navigation dengan pill status interaktif dan specular light highlight di tiap node antarmuka.",
      "Desain Vertical Glass Rail Drawer dengan icon hover expansion, badge counter live, dan aksen amethyst glow.",
      "Ciptakan Radial Satellite Navigation Ring dengan menu melingkar yang mengorbit node pusat.",
      "Rancang Segmented Horizontal Tab Strip dengan moving glass highlight indicator di bawah tab aktif."
    ],
    "dashboards": [
      "Desain Obsidian Telemetry Command Matrix (max-width: 720px) dengan dual-column telemetry grid, CPU core live bar, dan network ping readout.",
      "Rancang Realtime System Cockpit dengan mini sparklines, status cluster server, dan depth glass border asimetris.",
      "Ciptakan Multi-Pane Analytics Workbench dengan kartu metrik modular, filter rentang waktu, dan chart preview.",
      "Desain Cloud Infrastructure Overview Board dengan peta node server global dan latency gauge."
    ],
    "scenery": [
      "Ciptakan Glass Scenery Workstation Viewport (max-width: 820px) berisi komposit panel multi-widget: compute metrics, memory status, dan quick command dock.",
      "Desain Cybernetic Multi-Widget Viewport dengan layout komposit pemandangan antarmuka yang memukau.",
      "Rancang Autonomous Studio Viewport dengan split panel editor visual, status terminal, dan inspector kaca.",
      "Ciptakan Modular Environment Scenery Hub dengan grid workstation responsif bertingkat kedalaman optik."
    ],
    "inputs": [
      "Rancang Intelligent Semantic Prompt Bar dengan tag pencarian interaktif (#Specular, #AuroraMesh), icon Lucide terminal, dan glowing focus ring.",
      "Ciptakan Floating Command Input Cluster dengan tombol submit terintegrasi dan ambient depth blur.",
      "Desain Dual Token Input Bar dengan selector model AI dropdown di dalam form dan counter karakter live.",
      "Ciptakan Glass Expandable Search Omnibox dengan auto-complete suggestions panel yang muncul mengapung."
    ],
    "feedback": [
      "Ciptakan Glass Password Strength Glowing Meter dengan bar segmen 4-warna bercahaya (Emerald, Solar Amber, Ruby) dan feedback enkripsi.",
      "Rancang Solar Amber Notification Pill dengan refractive glass blur dan auto-dismiss spring interaction.",
      "Desain Floating Specular Glass Toast Alert dengan progress countdown bar dan dismiss swipe gesture.",
      "Ciptakan Prismatic Status Badge Group dengan pulsating status beacons dan tooltip micro-overlay."
    ],
    "other": [
      "Ciptakan Experimental Radial Command Wheel dengan circular touch hotspots dan holographic optic target di tengah.",
      "Rancang Prismatic Glass Resonance Orb dengan kontrol interaktif orisinal bebas di kategori 'other'.",
      "Desain Kinetic Gyroscope Data Sphere dengan rotasi interaktif 3D dan optic lens focus.",
      "Ciptakan Holographic Quantum Coordinate Matrix dengan aksen spectral-prismatic dan interaktivitas unik."
    ]
  };

  var prompts = categoryDirectives[category];
  if (!prompts || prompts.length === 0) {
    prompts = categoryDirectives["other"];
  }
  var idx = Math.floor(Math.random() * prompts.length);
  return prompts[idx];
}

/**
 * Trigger Otomatis Berulang (Cron Trigger)
 * Frekuensi bisa diatur di Triggers (Ikon Jam):
 * - Minutes timer: Every 5 minutes, Every 10 minutes, Every 15 minutes, Every hour
 *
 * Tiap kali jalan, fungsi ini men-dispatch variasi batch otonom dengan kategori berbeda ke GitHub Actions.
 */
function autonomousCronTrigger() {
  Logger.log("Menjalankan siklus otonom cloud Prototype...");
  
  var CATEGORIES = ["sliders", "telemetry", "controls", "navigation", "buttons", "dashboards", "scenery", "inputs", "feedback", "other"];
  // Acak urutan kategori agar tiap siklus menghasilkan variasi baru
  for (var i = CATEGORIES.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = CATEGORIES[i];
    CATEGORIES[i] = CATEGORIES[j];
    CATEGORIES[j] = temp;
  }

  var BATCH_COUNT = 2; // Jumlah batch per siklus
  for (var k = 0; k < BATCH_COUNT; k++) {
    var cat = CATEGORIES[k % CATEGORIES.length];
    var prompt = generateAutonomousPrompt(cat);
    Logger.log("Dispatching autonomous batch item #" + (k + 1) + " (" + cat + "): " + prompt.substring(0, 75) + "...");
    dispatchToGitHub(prompt, cat, "Rujuk ui/components/glass/STYLE_SPEC.md dan css.css. Pastikan bentuk form factor unik sesuai kategori dan bukan sekadar kotak generik!");
    if (k < BATCH_COUNT - 1) {
      Utilities.sleep(1500); // jeda antar dispatch
    }
  }
}
