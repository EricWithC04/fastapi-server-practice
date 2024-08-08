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
                {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
                {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
                {"role": "user", "content": data},
            ]
            
            # Inicia el streaming de la respuesta
            completion = client.chat.completions.create(
                model="lmstudio-ai/gemma-2b-it-GGUF",
                messages=history,
                temperature=0.7,
                stream=True,
            )

            new_message = {"role": "assistant", "content": ""}
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    # Enviar cada fragmento al cliente
                    await websocket.send_text(chunk.choices[0].delta.content)
                    new_message["content"] += chunk.choices[0].delta.content

            history.append(new_message)

    except WebSocketDisconnect:
        print("Client disconnected")