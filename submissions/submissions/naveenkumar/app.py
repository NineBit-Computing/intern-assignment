import streamlit as st
from utils.processor import analyze_resume

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")

st.title("🧠 Resume Analyzer & Job Matcher")
st.markdown("""
Upload your resume text below. The app will extract skills and experience and suggest matching job roles using AI (simulated here).
""")

with st.expander("📄 Sample Resume Format"):
    st.code(open("data/sample_resume.txt").read(), language="text")

resume_text = st.text_area("Paste your resume text here:", height=300)

if st.button("🔍 Analyze Resume"):
    if resume_text.strip() == "":
        st.warning("⚠️ Please paste your resume content.")
    else:
        result = analyze_resume(resume_text)

        st.success("✅ Analysis Complete")

        with st.expander("🧠 Extracted Details"):
            st.json(result)

        st.markdown("### 💼 Suggested Job Roles")
        for role in result["Suggested_Roles"]:
            st.markdown(f"- {role}")
