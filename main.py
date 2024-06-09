from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Use environment variables
client = AzureOpenAI(
  azure_endpoint=os.getenv("AZURE_ENDPOINT"),
  api_key=os.getenv("API_KEY"),
  api_version="2024-02-01"
)

def chat_with_system(client):
    conversation = [
        {"role": "system", "content": "Welcome to the Erasmus Information Bot. How can I assist you with your Erasmus inquiries today?"},
    ]

    while True:
        user_message = input("You: ")
        conversation.append({"role": "user", "content": user_message})

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
                            "strictness": 10,
                            "top_n_documents": 128,
                            "authentication": {
                                "type": "api_key",
                                "key": os.getenv("SEARCH_API_KEY")
                            },
                            "key": os.getenv("SEARCH_API_KEY"),
                        }
                    }
                ],
            },
        )

        system_response = response.choices[0].message.content
        print("System:", system_response)

        if user_message.lower() == "stop":
            break

        conversation.append({"role": "assistant", "content": system_response})

chat_with_system(client)
