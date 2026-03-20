# docs/

This folder contains screenshots and any additional documentation assets for the project.

## Required screenshots

After running the app locally, take screenshots of both pages and save them here:

| File | Page | How to capture |
|---|---|---|
| `upload.png` | Upload / home page (`/`) | Open http://127.0.0.1:8000/ and screenshot |
| `result.png` | Prediction result page (`/predict`) | Upload any image and screenshot the result |

Once added, they will be embedded in the main `README.md`:

```md
![Upload page](docs/upload.png)
![Result page](docs/result.png)
```

## How to run the app for screenshots

```bash
python -m venv .venv
source .venv/bin/activate        # mac/linux
# .venv\Scripts\activate         # windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/ in your browser.
