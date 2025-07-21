from flask import Flask, request, jsonify, send_from_directory
from main import ask_query, update_rag_with_human_input # Import your functions from main.py

app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Route for handling user questions
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': "Please provide a question."}), 400

    answer = ask_query(question)
    
    # Check for the specific string indicating human input is needed
    if answer == "NOT_RELEVANT_REQUEST_HUMAN_INPUT":
        # The frontend will check for the presence of this specific string
        # and then display the human input area.
        return jsonify({'answer': "I’m not sure. Please contact support.", 'needs_human_input': True})
    
    return jsonify({'answer': answer, 'needs_human_input': False})

# Route for submitting human answers
@app.route('/human-answer', methods=['POST'])
def human_answer():
    data = request.get_json()
    question = data.get('question', '')
    human_response = data.get('answer', '')

    if not question or not human_response:
        return jsonify({'response': "Missing question or human answer."}), 400

    reply = update_rag_with_human_input(question, human_response)
    return jsonify({'response': reply})

if __name__ == '__main__':
    # Ensure debug is False in production
    app.run(debug=True, port=5000) # You can specify a port if needed