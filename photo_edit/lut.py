# import numpy as np
# from scipy.ndimage import map_coordinates

# def load_cube_lut(path):
#     """
#     Load .cube 3D LUT into numpy array (size x size x size x 3)
#     Handles GMIC headers (TITLE, DOMAIN_*, etc.)
#     """
#     data = []
#     size = None

#     with open(path, "r") as f:
#         for line in f:
#             line = line.strip()
#             if not line or line.startswith("#"):
#                 continue
#             parts = line.split()
#             if parts[0].upper() == "LUT_3D_SIZE":
#                 size = int(parts[1])
#             elif parts[0].upper().startswith("DOMAIN_"):
#                 continue
#             elif parts[0].upper() == "TITLE":
#                 continue
#             else:
#                 try:
#                     vals = list(map(float, parts))
#                     data.append(vals)
#                 except ValueError:
#                     continue

#     if size is None:
#         raise ValueError("LUT size not found in file.")
#     data = np.array(data).reshape((size, size, size, 3))
#     return data

# def apply_lut_trilinear(img, lut, strength=1.0):
#     """
#     Apply a 3D LUT to an image using trilinear interpolation.
    
#     img: HxWx3 float in [0,1]
#     lut: 3D LUT array
#     strength: 0..1, how much of LUT to apply
#     """
#     size = lut.shape[0]
#     coords = (img * (size - 1)).clip(0, size - 1 - 1e-6)
#     coords = coords.transpose(2,0,1)  # channels first for map_coordinates

#     out = np.zeros_like(img)
#     for c in range(3):
#         out[...,c] = map_coordinates(lut[...,c], coords, order=1, mode='nearest')
    
#     # Blend with original image
#     out = img * (1 - strength) + out * strength
#     return np.clip(out, 0, 1)


# def apply_lut(img, lut):
#     """
#     Apply a 3D LUT to an image (HxWx3 float in [0,1])
#     """
#     size = lut.shape[0]
#     coords = (img * (size - 1)).clip(0, size - 1 - 1e-6)

#     r_idx = coords[..., 0].astype(int)
#     g_idx = coords[..., 1].astype(int)
#     b_idx = coords[..., 2].astype(int)

#     out = lut[r_idx, g_idx, b_idx]
#     return np.clip(out, 0, 1)


import numpy as np
import torch
from scipy.ndimage import map_coordinates

def load_cube_lut(path):
    data, size = [], None
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = line.split()
            if parts[0].upper() == "LUT_3D_SIZE":
                size = int(parts[1])
            elif parts[0].upper().startswith("DOMAIN_") or parts[0].upper() == "TITLE":
                continue
            else:
                try: data.append(list(map(float, parts)))
                except ValueError: continue
    if size is None: raise ValueError("LUT size not found")
    return np.array(data).reshape((size,size,size,3))

def apply_lut_trilinear(img, lut, strength=1.0):
    size = lut.shape[0]
    coords = (img*(size-1)).clip(0, size-1-1e-6)
    coords = coords.transpose(2,0,1)
    out = np.zeros_like(img)
    for c in range(3):
        out[...,c] = map_coordinates(lut[...,c], coords, order=1, mode='nearest')
    return np.clip(img*(1-strength) + out*strength, 0, 1)

def apply_lut_gpu(img, lut, strength=1.0, device=None):
    if device is None: device = 'cuda' if torch.cuda.is_available() else 'cpu'
    img_tensor = torch.from_numpy(img).permute(2,0,1).unsqueeze(0).to(device)
    size = lut.shape[0]
    lut_tensor = torch.from_numpy(lut).permute(3,0,1,2).unsqueeze(0).to(device)
    # normalize for grid_sample
    grid = img_tensor.permute(0,2,3,1)*2 - 1
    grid = grid.unsqueeze(0)
    img_out = torch.nn.functional.grid_sample(lut_tensor.float(), grid[0].unsqueeze(0),
                                              mode='bilinear', align_corners=True)
    img_out = img_out.squeeze().permute(1,2,0)
    img_out = img_tensor.squeeze().permute(1,2,0)*(1-strength) + img_out*strength
    return img_out.cpu().numpy().clip(0,1)

def apply_lut(img, lut):
    """
    Apply a 3D LUT to an image (HxWx3 float in [0,1])
    """
    size = lut.shape[0]
    coords = (img * (size - 1)).clip(0, size - 1 - 1e-6)

    r_idx = coords[..., 0].astype(int)
    g_idx = coords[..., 1].astype(int)
    b_idx = coords[..., 2].astype(int)

    out = lut[r_idx, g_idx, b_idx]
    return np.clip(out, 0, 1)