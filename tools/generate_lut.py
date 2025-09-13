import numpy as np
import os

def generate_teal_orange_lut(size=17, path="examples/cinematic.cube"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("# Simple Teal-Orange LUT (generated)\n")
        f.write(f"LUT_3D_SIZE {size}\n")
        f.write("DOMAIN_MIN 0.0 0.0 0.0\n")
        f.write("DOMAIN_MAX 1.0 1.0 1.0\n")

        # Write in R, G, B nested loops so file maps to lut[r,g,b] on read
        for r in range(size):
            for g in range(size):
                for b in range(size):
                    R = r / (size - 1)
                    G = g / (size - 1)
                    B = b / (size - 1)

                    # grading: teal shadows, orange highlights
                    lum = (R + G + B) / 3.0
                    shadow_boost = 1.0 - lum
                    highlight_boost = lum

                    R_out = np.clip(R + 0.15 * highlight_boost - 0.05 * shadow_boost, 0, 1)
                    G_out = np.clip(G + 0.05 * shadow_boost, 0, 1)
                    B_out = np.clip(B + 0.15 * shadow_boost - 0.05 * highlight_boost, 0, 1)

                    f.write(f"{R_out:.6f} {G_out:.6f} {B_out:.6f}\n")

    print(f"✅ LUT saved to {path}")

if __name__ == "__main__":
    generate_teal_orange_lut()
