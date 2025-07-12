# 🧠 Customer Feedback Analyzer using CIQ SDK

This project analyzes customer feedback using the [NineBit CIQ](https://www.npmjs.com/package/@ninebit/ciq) AI orchestration SDK. It extracts structured insights such as **sentiment**, **category**, and a short **summary** from raw customer comments.

---

## 🚀 Features

- 🤖 Uses CIQ's LLM orchestration to interpret unstructured text.
- 🧾 Converts feedback into structured JSON with sentiment, category, and summary.
- 🛠️ Includes fallback parsing logic in case of malformed CIQ response.
- 📂 Outputs results to a clean JSON file.

---

## 📦 Tech Stack

- **Node.js** (v18+ recommended)
- **CIQ SDK** - `@ninebit/ciq`
- **File System** - `fs`, `path`

---

## 🛠️ Setup & Usage

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/your-username/ciq-feedback-analyzer.git
cd ciq-feedback-analyzer
npm install
