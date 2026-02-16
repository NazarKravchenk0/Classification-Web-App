from io import BytesIO

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from app.ml.inference import predict_image, predict_topk

app = FastAPI(title="Image Classification Web App")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(BytesIO(content))

    label, conf = predict_image(img)
    top3 = predict_topk(img, k=3)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "filename": file.filename,
            "label": label,
            "confidence": f"{conf * 100:.2f}%",
            "top3": [(l, f"{c*100:.2f}%") for l, c in top3],
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}
