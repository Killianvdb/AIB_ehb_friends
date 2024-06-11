from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Use environment variables to configure the Azure client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    api_version="2024-02-01"
)

def chat_with_system(user_message, conversation):
    # Adding a context or extra information to the user's message before sending it to Azure
    contextual_message = "User asked: " + user_message + "after responding, give out the first line of Title before a \n  trictly at the end of your response, nothing else: 'Title:' don't say here's the title, just follow the format given, no description about the Title or anything else, just the Title."

    # Append the contextual message instead of the raw user message
    conversation.append({"role": "user", "content": contextual_message})

    response = client.chat.completions.create(
        model="killian",
        messages=conversation,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": "https://killian-ehb-ai.search.windows.net",
                        "index_name": "ehbsite",
                        "semantic_configuration": "default",
                        "query_type": "simple",
                        "fields_mapping": {},
                        "in_scope": True,
                        "role_information": "You are an AI assistant that helps people find information.",
                        "strictness": 5,
                        "top_n_documents": 128,
                        "authentication": {
                            "type": "api_key",
                            "key": os.getenv("SEARCH_API_KEY")
                        }
                    }
                }
            ],
        }
    )

    system_response = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": system_response})

    return system_response

@app.route('/')
def home():
    return render_template('ehbFriend.html')  # Make sure your HTML file is named 'index.html'

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    conversation = [
        {"role": "system", "content": "Welcome to the Erasmus Information Bot. How can I assist you with your Erasmus inquiries today?"}
    ]

    if user_message.lower() == "stop":
        return jsonify({'response': 'Chat ended.'})

    response_message = chat_with_system(user_message, conversation)
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(debug=True)
