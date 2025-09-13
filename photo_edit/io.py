import rawpy
import numpy as np
from PIL import Image
import os

def load_image(path):
    """
    Load image from JPEG/PNG or RAW file (.NEF, .CR2, .ARW, etc.)
    Returns HxWx3 float32 array in [0,1]
    """
    path = str(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.nef', '.cr2', '.arw', '.dng', '.rw2', '.raf'):
        raw = rawpy.imread(path)
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=16)
        return (rgb.astype(np.float32) / 65535.0).clip(0, 1)
    else:
        img = Image.open(path).convert("RGB")
        return (np.asarray(img, dtype=np.float32) / 255.0).clip(0, 1)

def save_image(img, path, quality=100):
    """
    Save float32 image [0,1] as JPEG
    """
    img = np.clip(img * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path, quality=quality)


# import cv2
# import rawpy
# import numpy as np

# def load_image(path):
#     path = str(path)
#     if path.lower().endswith(('.nef', '.cr2', '.arw', '.dng', '.raf', '.rw2')):
#         with rawpy.imread(path) as raw:
#             img = raw.postprocess()
#     else:
#         img = cv2.imread(path, cv2.IMREAD_COLOR)[:,:,::-1]  # BGR -> RGB
#     img = img.astype(np.float32)/255.0
#     return img

# def save_image(img, path):
#     img_8 = (img*255).astype(np.uint8)
#     img_bgr = img_8[:,:,::-1]
#     cv2.imwrite(str(path), img_bgr)
