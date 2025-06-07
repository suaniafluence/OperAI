import os
from typing import List
from openai import OpenAI
from fpdf import FPDF

from .config import get_settings

settings = get_settings()

client = OpenAI()

async def process_natural_language(text: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[{"role": "user", "content": text}],
        text={"format": {"type": "text"}},
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True,
    )
    return response.text

def generate_pdf(filename: str, lines: List[str]) -> str:
    os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
    path = os.path.join(settings.LOCAL_STORAGE_PATH, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in lines:
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output(path)
    return path
