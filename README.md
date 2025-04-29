# QR Adder

[![Build Status](https://github.com/chrissyhroberts/QR_adder/actions/workflows/build.yml/badge.svg)](https://github.com/chrissyhroberts/QR_adder/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

**QR Adder** is a simple, cross-platform desktop application that generates personalized PDF forms with embedded QR codes and human-readable ID numbers.

Designed for research studies, logistics, events, and any setting where you need to personalize forms with scannable codes.

---
<img width="476" alt="Screenshot 2025-04-29 at 10 34 49" src="https://github.com/user-attachments/assets/355b6299-3684-4f78-aa16-e3ea60978051" />

## ✨ Features

- Import a PDF form template
- Import a CSV file with IDs
- Automatically add QR codes and readable IDs
- Fully adjustable QR code position, size, and text formatting
- Live preview of the first entry
- Output:
  - Single combined PDF
- Cross-platform:
  - Windows `.exe`
  - macOS `.app` (zipped)
  - Linux binary
- Fully offline — no internet needed once installed

---

## 📦 Installation

Download the latest release from the [Releases page](https://github.com/chrissyhroberts/QR_adder/releases).

| Platform | File | Instructions |
|:---|:---|:---|
| Windows | `QR_Adder_Windows.exe` | Download and run |
| macOS | `QR_Adder_Mac.zip` | Download, unzip, run `QR Adder.app` |
| Linux | `QR_Adder_Linux` | Download, make executable (`chmod +x`), run |

## 🛡 Security Notes

- **Windows SmartScreen:**  
  You may see a \"Windows protected your PC\" warning. Click **More info → Run anyway** to continue.

- **macOS Gatekeeper:**  
  On first launch, right-click the app and choose **Open** to bypass the \"unidentified developer\" warning.

These messages appear because the app is unsigned and do not indicate a security risk.

---

## 💻 How to Use

1. Launch the app.
2. Select your **PDF template**.
3. Select your **CSV file** containing an `ID` column.
4. Adjust QR and text settings if needed.
5. Preview the first entry.
6. Choose an output folder.
7. Click **Generate PDFs**!

👉 Done! Each ID will generate a personalized form.

---

## 📋 CSV Requirements

- Your CSV file **must contain a column named** `ID`.
- Example format:

```csv
ID,Name
1234,John Doe
5678,Jane Smith
```

---

## 🛠️ Running from Source

If you prefer to run QR Adder directly from the Python source code:

### 1. Install Python

- Download and install **Python 3.11** or higher from [python.org](https://www.python.org/downloads/).
- Ensure you select **"Add Python to PATH"** during installation.

Check installation:

```bash
python --version
```

---

### 2. Clone or Download the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

Or download ZIP and extract manually.

---

### 3. (Optional) Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
```bash
venv\Scripts\activate
```

- **macOS/Linux:**
```bash
source venv/bin/activate
```

---

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 5. Run the Application

```bash
python QR_adder.py
```

👉 GUI opens — ready to use!

---

## ⚙️ Technical Details

- Python 3.11
- PyQt5 (GUI)
- pandas (CSV handling)
- PyMuPDF (PDF editing)
- qrcode (QR code generation)
- pillow (image handling)
- Built with PyInstaller
- Automated GitHub Actions builds

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and contribute!

---

## 🙏 Acknowledgments

Thanks to the open-source libraries that made this project possible!

- PyQt5
- PyMuPDF
- pandas
- qrcode
- pillow

