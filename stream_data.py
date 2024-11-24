from fastapi import WebSocket, WebSocketDisconnect
from openai import OpenAI

# Configuración del cliente OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# @app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Espera el prompt del cliente
            data = await websocket.receive_text()
            
            history = [
                {"role": "system", "content": "Eres un tutor inteligente de la asignatura '''Python para ciencias de datos'''', debes responder siempre preguntas relacionadas con python y la ciencias de datos. '''No respondas nada que no tenga que ver con python'''. Dame resupuestas cortas no superes los 50 caracteres e ignora las preguntas de seguimiento."},
                # {"role": "user", "content": "Presentate la primera vez que se habra el programa"},
                {"role": "user", "content": data},
            ]
            
            # Inicia el streaming de la respuesta
            completion = client.chat.completions.create(
                model="TheBloke/CodeLlama-7B-Instruct-GGUF",
                messages=history,
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}

            completed_text = ""

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    # Enviar cada fragmento al cliente
                    completed_text += chunk.choices[0].delta.content
                    await websocket.send_text(completed_text)
                    new_message["content"] += chunk.choices[0].delta.content

            history.append(new_message)

    except WebSocketDisconnect:
        print("Client disconnected")