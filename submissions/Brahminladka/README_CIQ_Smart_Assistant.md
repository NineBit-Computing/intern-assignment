
# 🤖 CIQ Smart Meeting Assistant

A unified assistant to transcribe live Google Meet meetings, summarize them using NineBit CIQ’s orchestration SDK, and email the structured summary to the user. It also allows PDF ingestion and question answering using RAG.

---

## 🚀 Features

- 🎤 **Live Audio Transcription**
- 📝 **Structured Meeting Summarization** via RAG (CIQ SDK)
- 📄 **PDF Upload + Ask Questions**
- 📧 **Auto-email Summary or Answer**
- 💻 Built with **Streamlit UI**

---

## 🧪 Use Cases

- Meeting minutes automation
- Project management call summaries
- Research paper Q&A
- Client interaction documentation

---

## 🗂️ Folder Structure

```
submissions/Brahminladka/
├── app.py                # Streamlit UI
├── summarizer.py         # RAG summarizer using CIQ
├── transcriber.py        # Live meeting transcriber
├── rag_helper.py         # PDF ingestion and QnA
├── email_sender.py       # Summary email sender
├── requirements.txt      # All dependencies
└── README.md             # This file
```

---

## 🛠️ How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add API Credentials

In `summarizer.py`, set your CIQ API Key:

```python
client = NineBitCIQClient(api_key="your_ciq_api_key")
```

In `email_sender.py`, configure your Gmail + App Password.

---

### 3. Run the App

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) to use the assistant.

---

## 💡 Features in Detail

### 🗣️ Live Meeting Summary

- Speak into your mic (or route Google Meet audio)
- Generates JSON summary with:
  - Title
  - Attendees
  - Topics Discussed
  - Decisions Made
  - Action Items
  - Sentiment

### 📄 PDF + Ask Questions

- Upload any PDF document
- Ask questions about the content
- Get instant answers via CIQ RAG
- Results emailed to you

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Streamlit** – frontend
- **NineBit CIQ SDK** – RAG/LLM
- **SpeechRecognition / Whisper** – transcription
- **smtplib** – email integration

---

## ✉️ Example Output

```json
{
  "Title": "Team Sprint Planning",
  "Attendees": ["Alice", "Bob", "Charlie"],
  "Topics Discussed": ["Feature rollout", "Bug prioritization"],
  "Decisions Made": ["Deploy by July 15"],
  "Action Items": [
    {"task": "Write tests", "owner": "Alice", "due_date": "2025-07-14"}
  ],
  "Sentiment": "Positive"
}
```

---

## 🔐 Security Notes

- Use `.env` or environment variables for sensitive info
- Don’t commit credentials
- Email via Gmail App Passwords (not real password)

---

## 🧑‍💻 Author

**Aman Tiwari**  
[GitHub: Brahminladka](https://github.com/Brahminladka)

---

## ✅ Submission

This project is submitted as part of the NineBit Internship Assignment.  
Folder: `submissions/Brahminladka`
