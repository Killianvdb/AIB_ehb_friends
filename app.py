from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import logging
from openai import AzureOpenAI

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    api_version="2024-02-01"
)

# Home route for the chat interface
@app.route('/')
def home():
    return render_template('ehbFriend.html')

# Endpoint to handle chat interactions
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Enhanced contextual introduction for clarity
    context_message = ("This conversation is specifically about programs, degrees, "
                       "and educational services at Erasmushogeschool Brussel (EHB). "
                       "Please frame your questions accordingly. If your question is not related to EHB, "
                       "you will receive a standard response indicating non-relevance.")

    # Combine context with the user message
    conversation = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_message}
    ]

    try:
        # Request OpenAI to process the conversation
        response = client.chat.completions.create(
            model="killian",  # Ensure you're using the correct model
            messages=conversation,
            max_tokens=150
        )
        system_response = response.choices[0].message.content

        # Determine if the response is related to EHB
        if "This question is not about Erasmushogeschool Brussel (EHB)." in system_response:
            return jsonify({"response": "This question is not about Erasmushogeschool Brussel (EHB)."})
        return jsonify({"response": system_response})
    except Exception as e:
        logging.error(f"Error handling request with Azure OpenAI: {e}")
        return jsonify({"error": "Failed to process your request."}), 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
