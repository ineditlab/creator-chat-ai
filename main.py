from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AQUÍ ESTÁ LA MAGIA: Ahora lee la llave secreta desde Render
api_key_render = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key_render)

class UserRequest(BaseModel):
    idea: str

SYSTEM_PROMPT = """
Eres el 'Asistente de Guiones Virales Inedit', un experto en retención para TikToks y Reels.
Tu objetivo es transformar la idea del usuario en un guion estructurado de 15 segundos.

ESTRUCTURA OBLIGATORIA:
[0:00 - 0:02] GANCHO: (Descripción visual) "Frase de hook potente"
[0:02 - 0:13] CUERPO: (Montaje rápido) "Valor principal"
[0:13 - 0:15] CTA: "Llamado a la acción"
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

@app.post("/generar-guion")
async def generar_guion(request: UserRequest):
    try:
        response = model.generate_content(f"Crea un guion viral con esta idea: {request.idea}")
        return {"resultado": response.text}
    except Exception as e:
        # Si Gemini falla, mandará el error exacto a Webflow para que sepamos qué pasa
        return {"resultado": f"Error interno de IA: {str(e)}"}

@app.get("/")
def home():
    return {"status": "Creator Chat vivo"}
