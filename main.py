# import argparse
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from tqdm import tqdm
# from photo_edit.pipeline import process_image

# def process_single(img_file, lut_path, output_folder, strength, dithering):
#     out_file = output_folder / img_file.name
#     process_image(str(img_file), str(lut_path), str(out_file),
#                   lut_strength=strength, dithering=dithering)

# def main():
#     parser = argparse.ArgumentParser(description="Auto-correct + LUT (single or batch, parallel)")
#     parser.add_argument("input", help="Path to input image or folder")
#     parser.add_argument("lut", help="Path to .cube LUT file")
#     parser.add_argument("output", help="Path to output file or folder")
#     parser.add_argument("--strength", type=float, default=1.0, help="LUT strength 0..1")
#     parser.add_argument("--no-dither", action="store_true", help="Disable dithering")
#     parser.add_argument("--threads", type=int, default=4, help="Number of parallel threads")
#     args = parser.parse_args()

#     input_path = Path(args.input)
#     output_path = Path(args.output)
#     dithering = not args.no_dither

#     if input_path.is_file():
#         process_image(str(input_path), str(args.lut), str(output_path),
#                       lut_strength=args.strength, dithering=dithering)
#     elif input_path.is_dir():
#         output_path.mkdir(parents=True, exist_ok=True)
#         supported_exts = (".jpg", ".jpeg", ".png", ".nef", ".cr2", ".arw", ".dng", ".raf", ".rw2")
#         img_files = [f for f in input_path.iterdir() if f.suffix.lower() in supported_exts]

#         print(f"⚡ Processing {len(img_files)} images using {args.threads} threads...")

#         # Parallel processing with progress bar
#         with ThreadPoolExecutor(max_workers=args.threads) as executor:
#             futures = {executor.submit(process_single, img, args.lut, output_path, args.strength, dithering): img
#                        for img in img_files}

#             for f in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="img"):
#                 f.result()  # raise exceptions if any

#         print(f"✅ Batch processing complete. Outputs saved to {output_path}")
#     else:
#         raise ValueError(f"Input path {input_path} not found.")

# if __name__ == "__main__":
#     main()



# import argparse
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from tqdm import tqdm
# from photo_edit.pipeline import process_image

# def process_single(img_file, lut_path, output_folder, strength, dithering, use_gpu):
#     out_file = output_folder / img_file.name
#     process_image(str(img_file), str(lut_path), str(out_file),
#                   lut_strength=strength, dithering=dithering, use_gpu=use_gpu)

# def main():
#     parser = argparse.ArgumentParser(description="Auto-correct + LUT (single/batch, GPU, threads, dithering)")
#     parser.add_argument("input")
#     parser.add_argument("lut")
#     parser.add_argument("output")
#     parser.add_argument("--strength", type=float, default=1.0)
#     parser.add_argument("--no-dither", action="store_true")
#     parser.add_argument("--threads", type=int, default=4)
#     parser.add_argument("--cpu", action="store_true", help="Force CPU")
#     args = parser.parse_args()

#     input_path, output_path = Path(args.input), Path(args.output)
#     dithering = not args.no_dither
#     use_gpu = not args.cpu

#     if input_path.is_file():
#         process_image(str(input_path), str(args.lut), str(output_path),
#                       lut_strength=args.strength, dithering=dithering, use_gpu=use_gpu)
#     elif input_path.is_dir():
#         output_path.mkdir(parents=True, exist_ok=True)
#         supported_exts = (".jpg",".jpeg",".png",".nef",".cr2",".arw",".dng",".raf",".rw2")
#         img_files = [f for f in input_path.iterdir() if f.suffix.lower() in supported_exts]

#         print(f"⚡ Processing {len(img_files)} images using {args.threads} threads...")
#         with ThreadPoolExecutor(max_workers=args.threads) as executor:
#             futures = {executor.submit(process_single, img, args.lut, output_path,
#                                        args.strength, dithering, use_gpu): img
#                        for img in img_files}
#             for f in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="img"):
#                 f.result()
#         print(f"✅ Batch processing complete. Outputs saved to {output_path}")
#     else:
#         raise ValueError(f"Input path {input_path} not found.")

# if __name__ == "__main__":
#     main()


import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from photo_edit.pipeline import process_image

def process_single(img_file, lut_path, output_file, lut_strength, dithering, use_gpu):
    process_image(str(img_file), str(lut_path), str(output_file),
                  lut_strength=lut_strength, dithering=dithering, use_gpu=use_gpu)

def main():
    parser = argparse.ArgumentParser(description="Auto-correct + LUT (GPU, threads, dithering)")
    parser.add_argument("input")
    parser.add_argument("lut")
    parser.add_argument("output")
    parser.add_argument("--strength", type=float, default=1.0)
    parser.add_argument("--no-dither", action="store_true")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--cpu", action="store_true", help="Force CPU")
    args = parser.parse_args()

    input_path, output_base = Path(args.input), Path(args.output)
    dithering = not args.no_dither
    use_gpu = not args.cpu

    # LUT name for folder
    lut_name = Path(args.lut).stem
    output_folder = output_base.parent / lut_name / output_base.name if output_base.is_file() else output_base / lut_name
    output_folder.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        out_file = output_folder / input_path.name
        process_single(input_path, args.lut, out_file, args.strength, dithering, use_gpu)
        print(f"✅ Saved edited image to {out_file}")
    elif input_path.is_dir():
        supported_exts = (".jpg",".jpeg",".png",".nef",".cr2",".arw",".dng",".raf",".rw2")
        img_files = [f for f in input_path.iterdir() if f.suffix.lower() in supported_exts]

        print(f"⚡ Processing {len(img_files)} images with LUT '{lut_name}' using {args.threads} threads...")

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {executor.submit(process_single, img, args.lut, output_folder / img.name,
                                       args.strength, dithering, use_gpu): img for img in img_files}
            for f in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="img"):
                f.result()

        print(f"✅ Batch processing complete. Outputs saved to {output_folder}")
    else:
        raise ValueError(f"Input path {input_path} not found.")

if __name__ == "__main__":
    main()
