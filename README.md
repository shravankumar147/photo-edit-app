# 🎞️ Photo Edit App — Auto-Cinematic Photo Editor

A **free, open-source, automated photo editing app** for RAW and JPEG images that applies **auto exposure + cinematic LUTs**, supporting **GPU acceleration**, **multi-threaded batch processing**, and **dithering**. Think of it as a lightweight, scriptable Lightroom workflow.

---

## Why this project?

As a **photographer**, I love capturing beautiful moments.
As a **programmer**, I believe repetitive tasks should be automated.

Instead of spending hours in Lightroom manually fixing exposure and applying presets, I wanted a simple open-source tool that:

* 📂 Loads **RAW or JPEG** images
* 🔆 Auto-corrects **exposure & contrast**
* 🎨 Applies a **cinematic film LUT (.cube)**
* 💾 Exports a ready-to-share image

This project is my attempt to combine **artistry** with **automation**, making photo editing accessible, fast, and free.

---

## ✨ Features

* **Auto exposure / contrast stretch**
* **3D LUT application** (trilinear CPU fallback or GPU-accelerated via PyTorch)
* **LUT strength blending** (`--strength`)
* **Optional dithering** to reduce banding (`--no-dither`)
* **Batch folder processing** with multi-threading (`--threads`)
* **Progress bar** for large batches
* **Supports RAW + JPEG + PNG** images
* Automatically organizes output by **LUT name**

---

## 📂 Repo Layout

```
photo-edit-app/
│
├── main.py                 # CLI entry point
├── requirements.txt        # Dependencies
├── examples/
│   ├── sample.jpg
│   ├── cinematic.cube
│   └── cinematic/output.jpg
│
└── photo_edit/
    ├── __init__.py
    ├── pipeline.py         # Image processing pipeline
    ├── lut.py              # LUT load & GPU/CPU apply
    ├── corrections.py      # Auto exposure
    └── io.py               # Image load/save helpers
```

---

## ⚙️ Requirements

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```
numpy
opencv-python
rawpy
tqdm
scipy
torch
torchvision
```

---

## 🚀 Usage

### 1️⃣ Single Image

```bash
python main.py examples/sample.jpg examples/cinematic.cube examples/
```

* Output will automatically go into a **LUT-named folder**:

```
examples/cinematic/sample.jpg
```

---

### 2️⃣ Batch Folder

```bash
python main.py examples/input_folder examples/cinematic.cube examples/output_folder --threads 8 --strength 0.8
```

* Processes all supported images in `input_folder`
* Creates output folder:

```
examples/output_folder/cinematic/
```

* Adjustable LUT strength: `--strength 0.0..1.0`
* Force CPU instead of GPU: `--cpu`
* Disable dithering: `--no-dither`

---

## 📸 Example

**Input → Output (Cinematic LUT)**

<p align="center">
  <img src="examples/sample.jpg" alt="Input" width="45%">
  <img src="examples/cinematic/sample.jpg" alt="Cinematic Output" width="45%">
</p>  

---

## 📷 Supported Formats

* JPEG / PNG
* RAW: `.nef`, `.cr2`, `.arw`, `.dng`, `.raf`, `.rw2`

---

## 🔧 More Examples

### Single Image

```bash
python main.py examples/sample.jpg examples/fuji_fp-100c_alt.cube examples
```

* Output: `examples/fuji_fp-100c_alt/sample.jpg`

### Batch Folder

```bash
python main.py examples/input_folder examples/cinematic.cube examples/output_folder --threads 4
```

* Outputs: `examples/output_folder/cinematic/img1.jpg`, `img2.jpg`, …

---

## 📝 Notes

* **GPU acceleration** is automatic if CUDA is available.
* **Dithering** is optional but recommended to reduce color banding on smooth gradients.
* LUTs can be any `.cube` file (e.g., from GMIC presets or your own).
* Batch processing uses **multi-threading** to speed up CPU-bound tasks.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---
