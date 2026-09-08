/**
 * ==============================================================================
 * GlassOS Autonomous Generator — Google Apps Script (GAS) Cloud Gateway
 * ==============================================================================
 * ARCHITECTURE SECURITY NOTICE:
 * Do NOT hardcode API keys or webhook tokens in this script.
 * All sensitive secrets MUST be set in Apps Script:
 * File > Project Settings > Script Properties.
 *
 * Properties Required:
 * - GEMINI_API_KEY      : Google AI Studio API Key
 * - ROUTER_API_KEY      : 9Router / Custom OpenAI-compatible Gateway Token
 * - GITHUB_REPO_TOKEN   : GitHub Personal Access Token (for dispatching repository_dispatch)
 * - GITHUB_REPO         : "Fadhlijeu/prototype"
 * ==============================================================================
 */

function getSecret(key) {
  var props = PropertiesService.getScriptProperties();
  var val = props.getProperty(key);
  if (!val) {
    throw new Error("Missing required Script Property: " + key + ". Please configure it in Project Settings.");
  }
  return val;
}

/**
 * Webhook entrypoint (doPost)
 * Accepts directive tasks from remote curators, webhooks, or scheduled triggers.
 */
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var prompt = data.prompt || "Autonomous Glass UI Component";
    var category = data.category || "inputs";
    var directive = data.directive || "Explore new creative glass variations adhering to GlassOS tokens";

    // 1. Log incoming task
    Logger.log("Received task: " + prompt + " | Cat: " + category);

    // 2. Dispatch to GitHub Actions workflow via repository_dispatch
    var dispatchResult = dispatchToGitHub(prompt, category, directive);

    return ContentService.createTextOutput(JSON.stringify({
      status: "QUEUED",
      message: "Task successfully forwarded to GlassOS generator queue",
      dispatch: dispatchResult
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    Logger.log("Error in doPost: " + err.toString());
    return ContentService.createTextOutput(JSON.stringify({
      status: "ERROR",
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Sends a repository_dispatch event to GitHub Actions runner
 */
function dispatchToGitHub(prompt, category, directive) {
  var githubToken = getSecret("GITHUB_REPO_TOKEN");
  var repo = getSecret("GITHUB_REPO"); // e.g. "Fadhlijeu/prototype"
  
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
  if (code >= 200 && code < 300) {
    return { success: true, code: code };
  } else {
    return { success: false, code: code, body: response.getContentText() };
  }
}

/**
 * Scheduled trigger function (runs hourly or daily if installed)
 */
function autonomousCronTrigger() {
  Logger.log("Running autonomous generator scheduled pulse...");
  var seeds = [
    "Aurora glowing segmented stepper with fluid spring interaction",
    "Liquid frosted navigation dock with adaptive blur highlight",
    "Floating telemetry telemetry mini-gauge with animated specular dial",
    "Obsidian glass toast notification with subtle border shimmer"
  ];
  var randomSeed = seeds[Math.floor(Math.random() * seeds.length)];
  dispatchToGitHub(randomSeed, "autonomous", "Explore fresh glass interaction paradigms");
}
