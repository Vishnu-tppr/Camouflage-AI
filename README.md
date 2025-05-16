# 🖼️ Camouflage AI – Smart Video Background Remover 🎥🧠

> 🎯 An AI-powered desktop tool for removing video backgrounds using **YOLOv8 segmentation**.

> 🎨 Choose solid colors, images, or blur effects as your new backdrop — it's fast, clean, and stunningly simple!

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [📸 Demo Screenshots](#-demo-screenshots)
- [🧠 How It Works](#-how-it-works)
- [📁 File Structure](#-file-structure)
- [⚙️ Requirements](#-requirements)
- [🚀 How to Run](#-how-to-run)
- [🧩 Technologies Used](#-technologies-used)
- [👨🏻‍💻 Author](#-author)
- [📜 License](#-license)

---

## ✨ Features

- 🧍‍♂️ **AI-Powered Person Segmentation** – Detects humans using `YOLOv8n-seg`.
- 🎨 **Background Options**:
  - Solid color picker 🎨
  - Custom background image 🖼️
  - Gaussian blur effect 🔍
- 📂 **Video File Input** – Select and process any video file.
- 🔄 **Progress Tracking** – Real-time status updates with loading bars.
- 🧠 **Lightweight YOLOv8n Model** – Fast, accurate, and ideal for personal devices.
- 🖥️ **Cross-compatible** – Works on both CPU and GPU environments.

---

## 📸 Demo Screenshots
![Screenshot 2025-05-16 224741](https://github.com/user-attachments/assets/19f6379f-be12-48da-9900-4fb0ae2a0f38)
![Screenshot 2025-05-16 221116](https://github.com/user-attachments/assets/2fb29eda-9f6b-49df-9951-e57cb9d0dc70)
![Screenshot 2025-05-16 221130](https://github.com/user-attachments/assets/75556332-15d5-4bed-9807-89564494235d)
![Screenshot 2025-05-16 221258](https://github.com/user-attachments/assets/d03c90df-c265-465c-b248-6face805e649)
![Screenshot 2025-05-16 225424](https://github.com/user-attachments/assets/d095e2c9-99a3-4645-8a66-608d62c512ae)
![Screenshot 2025-05-16 221314](https://github.com/user-attachments/assets/db1e042d-a354-4409-8a34-2ba9bd74be3a)
![Screenshot 2025-05-16 221333](https://github.com/user-attachments/assets/1455e6b6-00af-4637-9838-05b10228b259)
![Screenshot 2025-05-16 221835](https://github.com/user-attachments/assets/d3feec9f-510c-4694-a3e8-e88070b16726)
![Screenshot 2025-05-16 225528](https://github.com/user-attachments/assets/0d7c12b9-4567-447f-a32e-62e41f6e3883)



---

## 🧠 How It Works

### 1️⃣ YOLOv8 Segmentation

```python
from ultralytics import YOLO
model = YOLO("yolov8n-seg.pt")
results = model.track(frame, persist=True, classes=0)
````

Detects the person (class ID 0) and generates binary masks for each frame.

---

### 2️⃣ Background Replacement

Based on your choice:

* **Color**: Overlays the mask with the selected RGB color.
* **Image**: Resizes and merges a new image background.
* **Blur**: Applies `cv2.GaussianBlur()` behind the person.

```python
mask = masks[0]
inverse_mask = cv2.bitwise_not(mask)
foreground = cv2.bitwise_and(frame, frame, mask=mask)
background = cv2.bitwise_and(chosen_bg, chosen_bg, mask=inverse_mask)
final = cv2.add(foreground, background)
```

---

## 📁 File Structure

```
📦 CamouflageAI/
 ┣ 📄 Camouflage AI.py         # GUI App using CustomTkinter
 ┣ 📄 process_video.py         # Main processing logic with YOLO
 ┣ 📄 requirements.txt         # Dependencies
 ┗ 📄 README.md                # You’re here!
```

---

## ⚙️ Requirements

Install all required packages with:

```bash
pip install -r requirements.txt
```

**Or manually:**

```bash
pip install customtkinter opencv-python numpy rembg pillow tkinter moviepy matplotlib scikit-image tqdm pyperclip
```

📝 Tested with Python 3.10+ on Windows

---

## 🚀 How to Run

```bash
python "Camouflage AI.py"
```

✅ Make sure `process_video.py` is in the same directory.
🖼️ Output videos are automatically saved in the `output/` folder.

---

## 🧩 Technologies Used

* [Python 3](https://www.python.org/)
* [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
* [OpenCV](https://opencv.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [NumPy](https://numpy.org/)
* [Pillow (PIL)](https://pypi.org/project/Pillow/)
* [Torch (PyTorch)](https://pytorch.org/)

---

## 👨🏻‍💻 Author

Made with ❤️ by [**Vishnu**](https://www.linkedin.com/in/vishnu-v-31583b327/)

> “Build with passion, debug with precision.” 🔥

---

## 📜 License

This project is open-source and licensed under the **MIT License**.

---

🌟 If you found this useful, leave a ⭐ on the repo and share it!

```
