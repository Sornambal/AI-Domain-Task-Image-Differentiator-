import io
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

sys.path.append(str(Path(__file__).resolve().parent))
from main import app

# Create two minimal PDF files from simple images
for name, color in [('a', (255, 255, 255)), ('b', (240, 240, 240))]:
    img = Image.new('RGB', (100, 100), color)
    buf = io.BytesIO()
    img.save(buf, format='PDF')
    buf.seek(0)
    Path(f'test_{name}.pdf').write_bytes(buf.read())

client = TestClient(app)
with open('test_a.pdf', 'rb') as fa, open('test_b.pdf', 'rb') as fb:
    resp = client.post('/api/compare', files={
        'image_a': ('test_a.pdf', fa, 'application/pdf'),
        'image_b': ('test_b.pdf', fb, 'application/pdf'),
    })
    print('status', resp.status_code)
    print('text', resp.text)
    try:
        print('json', resp.json())
    except Exception as e:
        print('json error', e)
