# import numpy as np
# from .io import load_image, save_image
# from .corrections import auto_exposure
# from .lut import load_cube_lut, apply_lut_trilinear

# def process_image(input_path, lut_path, output_path, lut_strength=1.0, dithering=True):
#     # Load image (RAW or JPEG)
#     img = load_image(input_path)

#     # Auto exposure
#     img = auto_exposure(img)

#     # Load LUT and apply trilinear interpolation
#     lut = load_cube_lut(lut_path)
#     img = apply_lut_trilinear(img, lut, strength=lut_strength)

#     # Optional dithering to reduce banding
#     if dithering:
#         noise = np.random.normal(0, 1/255, img.shape)
#         img = np.clip(img + noise, 0, 1)

#     # Save output
#     save_image(img, output_path)
#     print(f"✅ Saved edited image to {output_path}")


from .io import load_image, save_image
from .corrections import auto_exposure
from .lut import load_cube_lut, apply_lut_trilinear, apply_lut_gpu
import numpy as np

def process_image(input_path, lut_path, output_path, lut_strength=1.0, dithering=True, use_gpu=True):
    img = load_image(input_path)
    img = auto_exposure(img)
    lut = load_cube_lut(lut_path)
    if use_gpu:
        img = apply_lut_gpu(img, lut, strength=lut_strength)
    else:
        img = apply_lut_trilinear(img, lut, strength=lut_strength)
    if dithering:
        img = np.clip(img + np.random.normal(0, 1/255, img.shape), 0, 1)
    save_image(img, output_path)
