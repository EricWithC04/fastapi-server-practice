# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": """Sos un tutor inteligente experto en programacion y en el lenguaje Python. Vas a responder sobre temas que esten relacionados unicamente con python. Si te preguntan sobre otro tema que no tenga que ver con programacion o sea otro lenguaje que no sea python, responde amablemente que solo respondes sobre temas de python. Responde solo lo que te preguntan. Mantene el contexto solo cuando sea necesario. 
    
    """},
    {"role": "user", "content": "Hola, preséntate a alguien que abre este programa por primera vez. Sé conciso."},
]

while True:
    completion = client.chat.completions.create(
        model="lmstudio-ai/gemma-2b-it-GGUF",
        messages=history,
        temperature=0.1,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    prompt = input("> ")
    history.append({"role": "user", "content": prompt})

