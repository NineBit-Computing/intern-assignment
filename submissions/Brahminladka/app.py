import streamlit as st
from transcriber import transcribe_meeting
from summarizer import summarize_transcript
from email_sender import send_summary_email
from rag_helper import ingest_pdf, ask_pdf_query

st.set_page_config("CIQ Smart Assistant", layout="centered")
st.title("🤖 CIQ Smart Meeting Assistant")

with st.form("meeting_form"):
    meet_link = st.text_input("🔗 Google Meet Link")
    email = st.text_input("📧 Your Email")
    action = st.radio("Choose Action", ["Live Meeting Summary", "Ask Question from PDF"])
    question = st.text_input("💬 Ask a Question (only for PDF mode)")
    uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])
    submit = st.form_submit_button("🚀 Run")

if submit:
    if action == "Live Meeting Summary":
        st.info("🎤 Transcribing live audio... Speak now. Stop with Ctrl+C.")
        transcript = transcribe_meeting()

        st.info("📄 Generating structured summary...")
        summary = summarize_transcript(transcript)

        st.success("✅ Summary Ready:")
        st.json(summary)

        send_summary_email(email, summary)
        st.success("📩 Sent to your email!")

    elif action == "Ask Question from PDF":
        if uploaded_file and question:
            st.info("📥 Ingesting PDF...")
            ingest_pdf(uploaded_file)

            st.info("🔍 Asking question...")
            answer = ask_pdf_query(question)

            st.success("✅ Answer:")
            st.write(answer)

            send_summary_email(email, {"Question": question, "Answer": answer})
            st.success("📩 Answer sent to your email!")
        else:
            st.error("Please upload a PDF and enter a question.")
