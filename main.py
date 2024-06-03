from openai import AzureOpenAI # Import the AzureOpenAI class from the openai module

def chat_with_system(client): # Define a function called chat_with_system that takes in a client as an argument
    conversation = [
        {"role": "system", "content": "Welcome to the Erasmus Information Bot. How can I assist you with your Erasmus inquiries today?"},
    ]

    while True:
        user_message = input("You: ")
        conversation.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="killian",  # The model to use for completion
            messages=conversation
        )

        system_response = response.choices[0].message.content
        print("System:", system_response)

        if user_message.lower() == "stop":
            break

        conversation.append({"role": "assistant", "content": system_response})

client = AzureOpenAI(
  azure_endpoint="https://killian-ehb-ai.openai.azure.com/", # The endpoint of the Azure OpenAI API
  api_key="8154f05ed6f94ea68f86c3610c13e702",  # The API key of the Azure OpenAI API
  api_version="2024-02-01" # The API version of the Azure OpenAI API
)

chat_with_system(client)
