from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List

from rag_logic import get_rag_response  # type: ignore

DOCS_DIR = Path(__file__).parent / "docs"
DOCS_DIR.mkdir(exist_ok=True)

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload_file(document: UploadFile = File(...)):
    if not document.filename.endswith((".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only .txt or .md files are allowed")
    contents = await document.read()
    dest = DOCS_DIR / document.filename
    with dest.open("wb") as f:
        f.write(contents)
    return {"detail": "uploaded"}


@app.post("/query")
async def query_endpoint(payload: QueryRequest):
    docs: List[str] = []
    for ext in ("*.txt", "*.md"):
        for file_path in DOCS_DIR.glob(ext):
            docs.append(file_path.read_text())

    paragraphs: List[str] = []
    for doc in docs:
        for para in doc.split("\n\n"):
            cleaned = para.strip()
            if cleaned:
                paragraphs.append(cleaned)

    answer = get_rag_response(payload.question, paragraphs)
    return JSONResponse({"response": answer})
