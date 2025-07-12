const fs = require("fs");
const path = require("path");
const { analyzeFeedback } = require("./utils/ciqProcessor");

// Path definitions
const inputPath = path.join(__dirname, "data", "feedback.json");
const outputPath = path.join(__dirname, "output", "results.json");

/**
 * Loads user feedbacks from feedback.json
 */
function loadFeedbacks() {
  try {
    return require(inputPath);
  } catch (err) {
    console.error("❌ Failed to load feedback.json:", err.message);
    return [];
  }
}

/**
 * Saves results to results.json
 */
function saveResults(results) {
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`✅ Done! Results saved to output/results.json`);
}

/**
 * Main analysis runner — loops through feedbacks and analyzes each.
 */
async function runAnalysis() {
  const feedbacks = loadFeedbacks();
  const results = [];

  for (let feedback of feedbacks) {
    console.log(`🔍 Analyzing: "${feedback}"`);
    const analysis = await analyzeFeedback(feedback);
    results.push({ original: feedback, analysis });
  }

  saveResults(results);
}

runAnalysis();
