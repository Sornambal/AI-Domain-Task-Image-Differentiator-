import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.append(str(Path(__file__).resolve().parent))

from services.diff_engine import detect_differences


def test_detect_differences_on_simple_change():
    a = np.zeros((200, 200, 3), dtype=np.uint8)
    b = np.zeros((200, 200, 3), dtype=np.uint8)
    b[50:100, 50:100] = 255

    stats = detect_differences(a, b)

    assert stats["num_changed_regions"] >= 1
    assert stats["percent_area_changed"] >= 0
    assert len(stats["regions"]) >= 1


if __name__ == "__main__":
    test_detect_differences_on_simple_change()
    print("diff_engine smoke test passed")
