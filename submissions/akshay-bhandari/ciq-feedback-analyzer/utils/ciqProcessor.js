// ciqProcessor.js

/**
 * CIQ Feedback Analyzer Module
 *
 * This module interfaces with the CIQ SDK to analyze customer feedback text.
 * It constructs a prompt, sends it to CIQ via `ragQuery`, and safely parses the response.
 * If parsing fails, it falls back to a basic key-value parser.
 */

const { CIQClient } = require("@ninebit/ciq");

// CIQ API Key: Use environment variable or fallback to default key for testing.
const apiKey = process.env.API_KEY || "db4c6444-1a16-46fb-98f6-9d74bd8c6fb2";
const client = new CIQClient(apiKey);

/**
 * Safely parses a potentially double/triple-stringified JSON string.
 * Attempts up to 3 levels of parsing.
 *
 * @param {string} raw - Raw response string from CIQ.
 * @returns {object} - Parsed object or error object.
 */
function safelyParse(raw) {
  try {
    let parsed = raw;

    // Attempt up to 3 levels of parsing if the content remains a string
    for (let i = 0; i < 3; i++) {
      if (typeof parsed === "string") {
        parsed = JSON.parse(parsed);
      } else {
        break;
      }
    }

    if (typeof parsed === "object" && parsed !== null) {
      return parsed;
    }

    throw new Error("Parsing did not yield a valid object.");
  } catch (e) {
    console.warn("❌ Failed to parse CIQ response:", raw);
    return { error: "Failed to parse CIQ response after multiple attempts" };
  }
}

/**
 * Main function to analyze a piece of customer feedback.
 * Builds prompt → queries CIQ → parses result → falls back if needed.
 *
 * @param {string} feedbackText - Raw user feedback.
 * @returns {Promise<object>} - Structured analysis result (sentiment, category, summary).
 */
async function analyzeFeedback(feedbackText) {
  const prompt = `
  You are a helpful assistant that analyzes customer feedback.
  
  Analyze this feedback:
  "${feedbackText}"
  
  Return only this JSON:
  {
    "sentiment": "Positive | Neutral | Negative",
    "category": "UI | Performance | Support | Features",
    "summary": "A short, clear summary of the feedback"
  }
  Strictly return valid JSON with double quotes. No explanation.
  `;

  const response = await client.ragQuery(prompt);
  const raw = response?.result || response;

  if (!raw) {
    console.warn("⚠️ No answer returned from CIQ.");
    return { error: "CIQ response missing or malformed" };
  }

  const parsed = safelyParse(raw);

  // If parsing fails, use fallback method
  if (parsed.error) {
    const fallback = parseFallbackResponse(raw);
    return fallback?.summary ? fallback : parsed;
  }

  return parsed;
}

/**
 * Fallback parser that extracts sentiment, category, and summary
 * from a plain-text key-value string format.
 *
 * @param {string} text - Raw response in human-readable format.
 * @returns {object} - Parsed fallback result.
 */
function parseFallbackResponse(text) {
  console.log("🔍 Fallback Parser Input:\n", text);
  try {
    const obj = {};
    const lines = text.trim().split("\n");

    for (let line of lines) {
      let [key, ...rest] = line.split(":");
      if (key && rest.length > 0) {
        obj[key.toLowerCase()] = rest.join(":").trim();
      }
    }

    return {
      sentiment: obj.sentiment || "Unknown",
      category: obj.category || "Uncategorized",
      summary: obj.summary || "No summary",
    };
  } catch (err) {
    return { error: "Failed to parse" };
  }
}

// Exported function to be used in index.js or other scripts
module.exports = { analyzeFeedback };
