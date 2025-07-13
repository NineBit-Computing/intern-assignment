from ninebit_ciq import NineBitCIQClient
import tempfile
import time

client = NineBitCIQClient(api_key="ddafd3b6-f5dc-4883-9465-7c5d3127e567")

ingestion_complete = False

def ingest_pdf(uploaded_file):
    global ingestion_complete
    ingestion_complete = False

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    def on_done(err, data):
        global ingestion_complete
        if err:
            print(f"❌ Ingestion error: {err}")
            ingestion_complete = False
        else:
            print("✅ PDF Ingested.")
            ingestion_complete = True

    client.ingest_file(file=tmp_path, callback=on_done)

    # Wait for ingestion to complete (max 10 seconds)
    for _ in range(10):
        if ingestion_complete:
            break
        time.sleep(1)

    if not ingestion_complete:
        raise RuntimeError("PDF ingestion did not complete in time.")

def ask_pdf_query(question):
    if not ingestion_complete:
        raise RuntimeError("PDF not ingested. Please ingest first.")
    try:
        return client.rag_query(query=question)
    except Exception as e:
        return {"error": f"RAG query failed: {e}"}
