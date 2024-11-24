# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="lmstudio-ai/gemma-2b-it-GGUF",
  messages=[
    {"role": "system", "content": "Eres un tutor inteligente de la asignatura '''Python para ciencias de datos'''', debes responder siempre preguntas relacionadas con python y la ciencias de datos. '''No respondas nada que no tenga que ver con python'''. Dame resupuestas cortas no superes los 50 caracteres e ignora las preguntas de seguimiento."},
    {"role": "user", "content": "Dame una función para sacar el maximo de 2 numero sin utilizar el metodo max"}
  ],
  temperature=0.1,
)

print(completion.choices[0].message)