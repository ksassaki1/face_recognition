# ──────────────────────────────────────────────────────────────────────────────
# Face Registration & Recognition — Jupyter Notebook
# ──────────────────────────────────────────────────────────────────────────────
# Notebook : face_registration_recognition.ipynb
#
# • Face enrolment  – extracts 128-D embeddings and saves them to encodings.pickle
# • Face recognition – labels faces in photos or a live webcam stream
# • Output versioning – writes recognized.jpg, recognized_1.jpg, recognized_2.jpg…
#
# Full Conda environment specified in environment.yml  (env name: facerec)
# ──────────────────────────────────────────────────────────────────────────────


# QUICK START
# ───────────

# 1 · Clone the repository
git clone https://github.com/<your-user>/face-registration-recognition.git
cd face-registration-recognition

# 2 · Create the Conda environment
conda env create -f environment.yml
conda activate facerec

# 3 · Launch the notebook
jupyter lab        # or: jupyter notebook


# FOLDER LAYOUT EXAMPLE (for batch enrolment)
# ────────────────────────────────────────────
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
# If you keep photos under dataset_faces/<PersonName>/,
# the notebook automatically uses the folder name as the label.


# MAIN NOTEBOOK SECTIONS
# ──────────────────────
# 3 · Batch enrolment            – scans dataset_faces/** and updates encodings.pickle
# 4 · Single-photo enrolment     – adds one image without losing existing data
# 5 · Recognition on image       – detects, labels, and writes recognized*.jpg
# 6 · Real-time recognition      – webcam preview (press “q” to quit)


# ADDING MORE FACES LATER
# ───────────────────────
# 1. conda activate facerec
# 2. Run section 4 (or section 3 if you added new folders)
# 3. encodings.pickle grows cumulatively — nothing is overwritten


# LICENSE
# ───────
# MIT License — see the LICENSE file
#
# ──────────────────────────────────────────────────────────────────────────────

