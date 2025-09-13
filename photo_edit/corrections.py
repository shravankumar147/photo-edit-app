import numpy as np

def auto_exposure(img, low=0.5, high=99.5):
    """
    Percentile-based auto exposure / contrast stretch.

    img: HxWx3 float image in [0,1]
    low/high: percentiles for clipping
    """
    p_low = np.percentile(img, low, axis=(0,1))
    p_high = np.percentile(img, high, axis=(0,1))

    # scale to [0,1] and clip
    img_adj = (img - p_low) / (p_high - p_low + 1e-6)
    return np.clip(img_adj, 0, 1)


# import numpy as np

# def auto_exposure(img, low=0.5, high=99.5):
#     """Percentile-based auto exposure / contrast stretch."""
#     p_low = np.percentile(img, low, axis=(0,1))
#     p_high = np.percentile(img, high, axis=(0,1))
#     img = (img - p_low) / (p_high - p_low)
#     return np.clip(img, 0, 1)
