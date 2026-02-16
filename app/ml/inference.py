import json
from pathlib import Path
from typing import List, Tuple

import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model.ts"
LABELS_PATH = ROOT / "labels.json"

_preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

_model = None
_labels: List[str] = []

def _load_labels() -> List[str]:
    if LABELS_PATH.exists():
        return json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    return ["class_0", "class_1"]

def _load_model(n_classes: int):
    if MODEL_PATH.exists():
        m = torch.jit.load(str(MODEL_PATH), map_location="cpu")
        m.eval()
        return m

    # Fallback model to keep app runnable before you export a real model
    class _Fallback(torch.nn.Module):
        def __init__(self, n: int):
            super().__init__()
            self.pool = torch.nn.AdaptiveAvgPool2d((1, 1))
            self.fc = torch.nn.Linear(3, n)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = self.pool(x).squeeze(-1).squeeze(-1)
            return self.fc(x)

    return _Fallback(n_classes).eval()

_labels = _load_labels()
_model = _load_model(len(_labels))

@torch.inference_mode()
def predict_image(img: Image.Image) -> Tuple[str, float]:
    if img.mode != "RGB":
        img = img.convert("RGB")

    x = _preprocess(img).unsqueeze(0)
    logits = _model(x)
    probs = torch.softmax(logits, dim=1)[0]
    conf, idx = torch.max(probs, dim=0)

    label = _labels[int(idx)] if 0 <= int(idx) < len(_labels) else "unknown"
    return label, float(conf)

@torch.inference_mode()
def predict_topk(img: Image.Image, k: int = 3) -> List[Tuple[str, float]]:
    if img.mode != "RGB":
        img = img.convert("RGB")

    x = _preprocess(img).unsqueeze(0)
    logits = _model(x)
    probs = torch.softmax(logits, dim=1)[0]

    k = max(1, min(k, probs.numel()))
    confs, idxs = torch.topk(probs, k=k)

    out: List[Tuple[str, float]] = []
    for c, i in zip(confs.tolist(), idxs.tolist()):
        label = _labels[int(i)] if 0 <= int(i) < len(_labels) else f"class_{int(i)}"
        out.append((label, float(c)))
    return out
