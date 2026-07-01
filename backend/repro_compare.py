import io
import sys
from pathlib import Path

from PIL import Image
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parent))
from main import app

client = TestClient(app)

img_a = Image.new('RGB', (100, 100), (255, 0, 0))
buf_a = io.BytesIO()
img_a.save(buf_a, format='PNG')
buf_a.seek(0)

img_b = Image.new('RGB', (100, 100), (0, 255, 0))
buf_b = io.BytesIO()
img_b.save(buf_b, format='PNG')
buf_b.seek(0)

resp = client.post('/api/compare', files={'image_a': ('a.png', buf_a, 'image/png'), 'image_b': ('b.png', buf_b, 'image/png')})
print(resp.status_code)
print(resp.text)
