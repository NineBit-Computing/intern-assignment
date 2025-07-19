from ninebit_ciq import NineBitCIQClient
from sentence_transformers import SentenceTransformer, util


# Initialize the NineBitCIQClient with an API key from environment variables
# Replace "YOUR_NINEBIT_CIQ_API_KEY" with your actual API key, or set it as an environment variable
# It's highly recommended to use environment variables for API keys in production
# export NINEBIT_CIQ_API_KEY="your_actual_api_key_here"
# client = NineBitCIQClient(api_key=os.getenv("NINEBIT_CIQ_API_KEY"))
client = NineBitCIQClient(api_key="6fe847d2-35ab-40e1-9e29-3e52a76f3f7d") # Replace with your actual key for testing

initial_qa_data = """ {"question": "How do I change my registered email address?", "answer": "You can update your email address from your account settings. Go to 'Profile' > 'Account Info' > 'Edit Email'. Verify with OTP to confirm changes. For assistance, contact HarsNet support at support@harsnet.com or call 1800-123-4567."}
{"question": "How can I update my phone number?", "answer": "To update your phone number, go to 'Profile' > 'Account Settings' > 'Phone Number'. Enter the new number and confirm via OTP. Need help? Email support@harsnet.com or call 1800-123-4567."}
{"question": "What should I do if my internet is not working?", "answer": "Please restart your modem/router. If the issue persists, check for outages in your area or contact HarsNet 24/7 support at support@harsnet.com or 1800-123-4567."}
{"question": "Why is my internet speed slow?", "answer": "Slow speed can be due to peak usage times, background apps, or router issues. Try restarting your router or moving closer to it. If the problem remains, contact HarsNet support at support@harsnet.com."}
{"question": "My video quality is poor despite fast internet. Why?", "answer": "Streaming apps may be set to 'Auto'. Adjust the settings to 'High Quality' manually. Also close background apps using bandwidth. For help, reach out to support@harsnet.com."}
{"question": "How do I change my service address?", "answer": "To change your address, go to 'My Account' > 'Service Details' > 'Change Address'. You may need to upload a valid proof of address. If needed, contact support@harsnet.com for guidance."}
{"question": "Can I pause my subscription temporarily?", "answer": "Yes, you can pause your subscription for up to 30 days. Go to 'My Plans' and select 'Pause'. Your billing will be adjusted accordingly. For any issues, email support@harsnet.com."}
{"question": "Is there a customer care number I can call?", "answer": "Yes, you can reach HarsNet customer support 24/7 at 1800-123-4567 or email us at support@harsnet.com."}
{"question": "Do you provide OTT bundles with the internet?", "answer": "Yes, HarsNet premium plans include OTT apps like Netflix, Prime Video, and Disney+ Hotstar. Check 'My Offers' in the HarsNet app or contact support@harsnet.com for more info."}
{"question": "How do I upgrade my plan?", "answer": "You can upgrade your plan anytime via the HarsNet app. Go to 'Plans' > 'Available Upgrades'. Changes apply instantly after confirmation. For help, contact support@harsnet.com or 1800-123-4567."}
"""

model = SentenceTransformer('all-MiniLM-L6-v2')

# Use a more descriptive name than 'str'
stored_data = initial_qa_data

def is_semantically_relevant(question, answer, threshold=0.20):
    """
    Checks the semantic similarity between a question and an answer.
    """
    embeddings = model.encode([question, answer], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    print(f"[Similarity Score] {similarity:.3f}")
    return similarity >= threshold

def ask_query(question):
    """
    Asks a question using the RAG system and checks for semantic relevance.
    """
    global stored_data # Acknowledge that we are modifying the global variable

    prompt = f"""
\"\"\"
You are a customer support AI assistant. Only use the given data to answer.
If you don't find a relevant answer, say: 'I’m not sure. Please contact support.'
Question: {question}
Knowledge Base:
{stored_data}
\"\"\"
"""
    try:
        response_from_rag = client.rag_query(query=prompt)
        # NineBitCIQClient's rag_query might return a dictionary or an object
        # If it returns a dict like {'answer': '...' }, you'd do response_from_rag['answer']
        
        # Check if the RAG response indicates no answer found
        if "I’m not sure. Please contact support." in response_from_rag:
            return response_from_rag # Directly return the "not sure" message

        if not is_semantically_relevant(question, response_from_rag):
            # If not semantically relevant, the Flask app should trigger human input
            # We return a specific string to indicate this to the Flask app
            return "NOT_RELEVANT_REQUEST_HUMAN_INPUT"
        return response_from_rag
    except Exception as e:
        print(f"[Error in ask_query] {e}")
        # Return a generic error message or the "not sure" message
        return "I’m not sure. Please contact support."
    

def update_rag_with_human_input(question, human_answer):
    """
    Updates the RAG knowledge base with a new question-answer pair from human input.
    """
    global stored_data # Acknowledge that we are modifying the global variable
    # Ensure the human_answer is properly escaped for JSON if it contains quotes
    escaped_human_answer = human_answer.replace('"', '\\"')
    new_entry = f'{{"question": "{question}", "answer": "{escaped_human_answer}"}}'
    stored_data += "\n" + new_entry
    print(f"[RAG Updated] New entry added for: {question}")
    return f"Thanks! I’ve updated my knowledge and here’s a human-style answer:\n{human_answer}"

# local testing of main.py
if __name__ == '__main__':
    # Example usage
    test_question = "How do I get faster internet?"
    answer = ask_query(test_question)
    print(f"\n[Bot Response for '{test_question}'] {answer}")

    if answer == "NOT_RELEVANT_REQUEST_HUMAN_INPUT" or "I’m not sure. Please contact support." in answer:
        print("\n[Simulation] Bot couldn't find a relevant answer or deemed it irrelevant.")
        human_correction = "You can upgrade your plan through the HarsNet app or contact support for higher speed options."
        updated_response = update_rag_with_human_input(test_question, human_correction)
        print(f"\n[Human Input Response] {updated_response}")
        # Now try asking the question again to see if it uses the new data
        answer_after_update = ask_query(test_question)
        print(f"\n[Bot Response after update for '{test_question}'] {answer_after_update}")