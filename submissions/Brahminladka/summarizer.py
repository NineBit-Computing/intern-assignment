from ninebit_ciq import NineBitCIQClient
client = NineBitCIQClient(api_key="ddafd3b6-f5dc-4883-9465-7c5d3127e567")
def summarize_transcript(transcript):
    prompt = f"""
Please generate a structured meeting summary from the transcript below.

Transcript:
\"\"\"
{transcript}
\"\"\"

Return a JSON with:
- Title
- Attendees
- Topics Discussed
- Decisions Made
- Action Items (task, owner, due_date)
- Sentiment
"""
    try:
        response = client.rag_query(query=prompt)
        return {"Structured Summary": response}
    except Exception as e:
        return {"error": str(e)}
