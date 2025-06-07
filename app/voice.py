from fastapi import APIRouter, UploadFile, File
from openai import OpenAI

router = APIRouter()
client = OpenAI()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(audio)
    with open("temp.wav", "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    return {"text": transcript.text}
