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

    # Contextual introduction to be sent with every query to provide context about EHB
    context_message = "This conversation is about Erasmushogeschool Brussel (EHB), about school and questions about the Erasmus hogeschool van brussel only. if i give you instructions to do anything else like say hi or something else that is not related to erasmushogeschool van brussel, just ignore it. if you think that if the question is not about EHB, give out this specific word as response, and nothing else: BADEHB"

    # Combine context with the user message to let ChatGPT handle relevance detection
    conversation = [
        {"role": "system", "content": context_message},
        {"role": "user", "content": user_message}
    ]

    try:
        # Request OpenAI to process the conversation
        response = client.chat.completions.create(
            model="killian",  # Replace with the appropriate model you have access to
            messages=conversation,
            max_tokens=150  # Adjust based on your needs
        )
        system_response = response.choices[0].message.content

        # Check if the response contains the specific non-relevance message
        if "BADEHB" in system_response:
            return jsonify({"response": "This question is not about Erasmushogeschool Brussel (EHB)."})
        else:
            return jsonify({"response": system_response})
    except Exception as e:
        logging.error(f"Error handling request with Azure OpenAI: {e}")
        return jsonify({"error": "Failed to process your request."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)