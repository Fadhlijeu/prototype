/**
 * ==============================================================================
 * GlassOS Autonomous Generator — Google Apps Script (GAS) Cloud Gateway
 * ==============================================================================
 * 
 * ARSITEKTUR & KEAMANAN:
 * 1. JANGAN PERNAH menuliskan API key langsung di file kode ini.
 * 2. Simpan semua kredensial di:
 *    Apps Script Editor > Project Settings (Ikon Gear) > Script Properties.
 *
 * SCRIPT PROPERTIES YANG DIBUTUHKAN:
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
    var data = JSON.parse(e.postData.contents);
    var prompt = data.prompt || "Aurora Glass Floating Input with Glow";
    var category = data.category || "inputs";
    var directive = data.directive || "Explore new creative glass variations adhering to GlassOS tokens";
    var mode = data.mode || "dispatch"; // 'dispatch' (ke GitHub Actions) atau 'direct' (generate langsung di GAS)

    if (mode === "direct") {
      // Generate langsung di serverless Apps Script menggunakan Gemini API
      var generatedOutput = generateWithGeminiDirect(prompt);
      return ContentService.createTextOutput(JSON.stringify({
        status: "GENERATED",
        prompt: prompt,
        output_snippet: generatedOutput.substring(0, 300) + "..."
      })).setMimeType(ContentService.MimeType.JSON);
    } else {
      // Default: Dispatch ke GitHub Actions runner
      var dispatchResult = dispatchToGitHub(prompt, category, directive);
      return ContentService.createTextOutput(JSON.stringify({
        status: "QUEUED",
        message: "Tugas berhasil diteruskan ke antrean GitHub Actions",
        dispatch: dispatchResult
      })).setMimeType(ContentService.MimeType.JSON);
    }

  } catch (err) {
    Logger.log("Error in doPost: " + err.toString());
    return ContentService.createTextOutput(JSON.stringify({
      status: "ERROR",
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Webhook Test Endpoint (doGet)
 * Menampilkan status ketersediaan gateway saat diakses via browser.
 */
function doGet() {
  return ContentService.createTextOutput(JSON.stringify({
    status: "ONLINE",
    service: "GlassOS Autonomous Generator Gateway (GAS)",
    timestamp: new Date().toISOString(),
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
    event_type: "glassos_generate_task",
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
 * METODE 2: Direct AI Call di Serverless Google (Gemini API)
 */
function generateWithGeminiDirect(prompt) {
  var apiKey = getSecret("GEMINI_API_KEY");
  var model = "gemini-1.5-flash"; // atau gemini-2.5-flash
  var url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent?key=" + apiKey;

  var systemInstruction = "You are GlassOS UI Architect. Generate complete single-file dark glassmorphism component HTML referencing ../css.css tokens and Lucide icons.";
  
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
 * Dapat dipasang di Apps Script: Triggers > Add Trigger > Time-driven > Every 1 hour / day.
 */
function autonomousCronTrigger() {
  Logger.log("Menjalankan siklus otonom cloud GlassOS...");
  var seeds = [
    "Floating glass telemetry dial gauge with specular illumination",
    "Liquid frosted breadcrumb navigation with spring pill indicators",
    "Obsidian glass segmented audio visualizer bar with live meter",
    "Aurora ambient gradient notification card with glass glow"
  ];
  var randomPrompt = seeds[Math.floor(Math.random() * seeds.length)];
  dispatchToGitHub(randomPrompt, "autonomous", "Explore fresh glass interaction paradigms");
}
