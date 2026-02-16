# Image Classification Web App (FastAPI)

Two-page web app:
1) Upload an image  
2) See prediction result (Top-1 + Top-3)

✅ ML logic is separated from the web part (`app/ml/inference.py`).  
✅ UI supports full-screen backgrounds like in the example screenshots.

---

## Dataset
- Link: <PASTE_DATASET_LINK_HERE>

## Google Colab training notebook
- Link: <PASTE_COLAB_LINK_HERE> (set access: anyone with link can view)

---

## Exported model files (IMPORTANT)

After training in Colab, download and place into:
- `app/ml/model.ts`  (TorchScript model)
- `app/ml/labels.json` (list of class names in correct order)

If `model.ts` is missing, the app uses a fallback dummy model so you can demo the UI,
but predictions will be meaningless until you export a real model.

---

## UI like the example (background images)

Replace these files with your images:
- `app/static/bg_upload.jpg`  (upload page background)
- `app/static/bg_result.jpg`  (result page background)

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .venv\Scripts\activate  # windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000/

---

## Project structure

```
classification_web_app_ui_like_example/
  app/
    main.py
    ml/
      inference.py
      labels.json
      model.ts        # <- add after training
    templates/
      upload.html
      result.html
    static/
      style.css
      bg_upload.jpg
      bg_result.jpg
  docs/
  requirements.txt
  README.md
```

---

## Screenshots for README (task requirement)
Run the app and make screenshots of:
- Upload page
- Result page

Put them in `docs/` and include here:
```md
![Upload](docs/upload.png)
![Result](docs/result.png)
```
