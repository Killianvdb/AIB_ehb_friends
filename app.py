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
    contextual_message = "User asked: " + user_message + "be as detailed as possible, don't begin your awnser with based on retrieved documents, just respond to the question, respond a good long prompt and keep a context that we talk about Erasmus hogeschool van Brussels, if you think the question isn't about erasmushogeschool, ask to ask a question about erasmushogeschool van Brussels, act as a personel of erasmushogeschool, don't awnser questions non related to erasmushogeschool van brussel, also respond in another language if there is another language in the prompt given"

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
                        "strictness": 3,
                        "top_n_documents": 7,
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


@app.route('/doc/<doc_id>')
def serve_document(doc_id):
    doc_filename_map = {
            "doc1": "toelatingsvoorwaarden.html",
            "doc2": "wat-kost-het.html",
            "doc3": "wat-kost-het.html",
            "doc4": "career-center.html",
            "doc5": "contact.html",
            "doc6": "info-voor-studiekiezers-ouders.html",
            "doc7": "info-voor-studiekiezers-ouders.html",
            "doc8": "info-voor-studiekiezers-ouders.html",
            "doc9": "info-voor-studiekiezers-ouders.html",
            "doc10": "infomomenten.html",
            "doc11": "opleidingen_technologisch-verpleegkundige.html",
            "doc12": "opleidingen_technologisch-verpleegkundige.html",
            "doc13": "opleidingen_technologisch-verpleegkundige.html",
            "doc14": "opleidingen_toerisme-recreatiemanagement.html",
            "doc15": "opleidingen_toerisme-recreatiemanagement.html",
            "doc16": "opleidingen_toerisme-recreatiemanagement.html",
            "doc17": "opleidingen_tourism-leisure-basics.html",
            "doc18": "opleidingen_tourism-leisure-basics.html",
            "doc19": "opleidingen_verpleegkunde.html",
            "doc20": "opleidingen_voedings-dieetkunde.html",
            "doc21": "opleidingen_vroedkunde.html",
            "doc22": "opleidingen_wat-zeg-jij.html",
            "doc23": "opleidingen_accounting-administration-e-learning.html",
            "doc24": "opleidingen_accounting-administration-e-learning.html",
            "doc25": "opleidingen_aan-de-slag-met-generatieve-ai-3-10-2024.html",
            "doc26": "opleidingen_applied-bio-informatics-research-diagnostics.html",
            "doc27": "opleidingen_applied-bio-informatics-research-diagnostics.html",
            "doc28": "opleidingen_artificial-intelligence-project-24-25.html",
            "doc29": "opleidingen_attest-rooms-katholieke-godsdienst-24-25.html",
            "doc30": "opleidingen_attest-rooms-katholieke-godsdienst-24-25.html",
            "doc31": "opleidingen_basisvorming-kwaliteitsvol-pedagogisch-werken-met-jonge-kinderen-24-25.html",
            "doc32": "opleidingen_bedrijfsverpleegkunde.html",
            "doc33": "opleidingen_big-data-iot-24-25.html",
            "doc34": "opleidingen_boekhouden-voor-werknemers-24-25.html",
            "doc35": "opleidingen_boekhouden-voor-werknemers-24-25.html",
            "doc36": "opleidingen_chatgpt-excel-24-10-2024.html",
            "doc37": "opleidingen_communicatie.html",
            "doc38": "opleidingen_communicatie.html",
            "doc39": "opleidingen_coding.html",
            "doc40": "opleidingen_cosmetic-sciences.html",
            "doc41": "opleidingen_cybersecurity-ethical-hacking.html",
            "doc42": "opleidingen_diabeteseducator.html",
            "doc43": "opleidingen_diabeteseducator.html",
            "doc44": "opleidingen_diversiteit-gelijkwaardigheid-inclusie-en-het-jonge-kind-24-25.html",
            "doc45": "opleidingen_dramatische-kunsten.html",
            "doc46": "opleidingen_educatieve-opleidingen-de-kunsten.html",
            "doc47": "opleidingen_educatieve-opleidingen-de-kunsten.html",
            "doc48": "opleidingen_elektromechanische-systemen.html",
            "doc49": "opleidingen_forensisch-verpleegkundig-expert.html"
    }

    filename = doc_filename_map.get(doc_id)
    if filename:
        return render_template(filename)
    else:
        return ConnectionAbortedError(404)  # Return a 404 Not Found error if the document ID is invalid

# Define other routes and functions as necessary

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
    app.run(debug=True, host='0.0.0.0')
