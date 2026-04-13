from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite que tu web (Webflow/Portal) se conecte sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# AIzaSyCpma-6vjU-gaNKiyJ6rXdF0PKLwCiD-o0
# ---------------------------------------------------------
genai.configure(api_key="TU_API_KEY_AQUI")

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
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

@app.post("/generar-guion")
async def generar_guion(request: UserRequest):
    try:
        response = model.generate_content(f"Crea un guion viral con esta idea: {request.idea}")
        return {"guion": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "Creator Chat vivo"}