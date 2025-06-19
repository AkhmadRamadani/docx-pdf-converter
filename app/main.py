from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import uuid
import subprocess
from threading import Thread
from .cleaner import auto_cleanup

UPLOAD_DIR = "/data/uploads"
OUTPUT_DIR = "/data/outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

# Start cleanup thread
Thread(target=auto_cleanup, args=(UPLOAD_DIR, OUTPUT_DIR, 600), daemon=True).start()

@app.post("/convert")
async def convert_docx_to_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        return {"error": "Only .docx files are supported"}

    input_filename = f"{uuid.uuid4()}.docx"
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", OUTPUT_DIR,
        input_path
    ], check=True)

    pdf_filename = input_filename.replace(".docx", ".pdf")
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    return FileResponse(pdf_path, filename=pdf_filename)
