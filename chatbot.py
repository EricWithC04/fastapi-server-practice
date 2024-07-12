# Example: reuse your existing OpenAI setup
from openai import OpenAI

def get_completion(prompt):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
    model="microsoft/Phi-3-mini-4k-instruct-gguf",
    messages=[
        {"role": "system", "content": "Eres un tutor inteligente de la asignatura 'Python para ciencias de datos', debes responder siempre preguntas relacionadas con python y la ciencias de datos. No respondas nada que no tenga que ver con python."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.1,
    )

    return completion.choices[0]
