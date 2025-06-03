# Face Registration & Recognition

A self-contained Jupyter notebook for **batch enrolment**, **single-image enrolment** and **real-time face recognition**.  
It extracts 128-D face embeddings (using *dlib* under the hood), stores them in `encodings.pickle`, and labels faces in images or a live webcam stream.

---

## Key features
- **Face enrolment** – generate and update 128-D embeddings for each person.  
- **Face recognition** – label faces on photos **or** use your webcam in real time.  
- **Output versioning** – recognised images are saved as `recognized.jpg`, `recognized_1.jpg`, `recognized_2.jpg`, …  
- **Reproducible environment** – a full Conda spec is provided in `environment.yml`.

---

## Quick Start

# 1 ▸ clone the repository
git clone https://github.com/ksassaki1/face_recognition.git
cd face_recognition

# 2 ▸ create & activate the Conda environment
conda env create -f environment.yml
conda activate facerec

# 3 ▸ launch the notebook
jupyter lab      # or: jupyter notebook


# ─────────────────────────────────────────────
# Folder layout (for batch enrolment)
# ─────────────────────────────────────────────
# .
# ├── dataset_faces/
# │   ├── Ana/
# │   │   ├── ana1.jpg
# │   │   └── ana2.jpg
# │   └── Carlos/
# │       ├── carlos1.png
# │       └── carlos2.jpg
# ├── face_registration_recognition.ipynb
# ├── environment.yml
# └── README.md
#


# MAIN NOTEBOOK SECTIONS
 ──────────────────────
# 3 ▸ Batch enrolment            – scans dataset_faces/** and updates encodings.pickle
# 4 ▸ Single-photo enrolment     – adds one image without losing existing data
# 5 ▸ Recognition on image       – detects, labels, and writes recognized*.jpg
# 6 ▸ Real-time recognition      – webcam preview (press “q” to quit)


# ADDING MORE FACES LATER
# ───────────────────────
# 1. conda activate facerec
# 2. Run section 4 (or section 3 if you added new folders)
# 3. encodings.pickle grows cumulatively — nothing is overwritten


# LICENSE
───────
# MIT License — see the LICENSE file

───────────────────────────────────────────────────────────────────────────────



