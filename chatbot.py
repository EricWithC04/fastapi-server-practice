from openai import OpenAI

def get_completion(prompt):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="lmstudio-ai/gemma-2b-it-GGUF",
    messages=[
        {"role": "system", "content": "Eres un tutor inteligente de la asignatura '''Python para ciencias de datos'''', debes responder siempre preguntas relacionadas con python y la ciencias de datos. '''No respondas nada que no tenga que ver con python'''. Dame resupuestas cortas no superes los 50 caracteres e ignora las preguntas de seguimiento."},
        {"role": "user", "content": prompt},
    ],
    temperature=0
    )

    return completion.choices[0]
