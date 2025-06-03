# Face Registration & Recognition Notebook

Small, self-contained Jupyter notebook that teaches you to **register faces and recognise them** with the popular [`face_recognition`](https://github.com/ageitgey/face_recognition) Python library.  
Everything lives in one file – `face_registration_recognition.ipynb`.

* Stores 128-D encodings for each person in a single `encodings.pickle`.  
* Lets you enrol people **from a folder tree** *or* **one photo at a time**.  
* Identifies faces in a still image (Section 4) or live webcam feed (Section 5).  

---

## Quick Preview

| Action | Screenshot |
|--------|------------|
| Enrolment from folders (`dataset_faces/PersonName/*.jpg`) | *add your own image* |
| Recognition result (`recognized.jpg`) | *add your own image* |

*(Drop a couple of images in `docs/` and update the links above if you want a real preview.)*

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/ksassaki1/face_recognition
cd face-registration-recognition

