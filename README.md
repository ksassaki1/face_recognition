###############################################################################
# Quick Start
###############################################################################

# 1 ▸ clone the repository
git clone https://github.com/ksassaki1/face_recognition.git
cd face_recognition

# 2 ▸ create & activate the Conda environment
conda env create -f environment.yml
conda activate facerec

# 3 ▸ launch the notebook
jupyter lab      # or: jupyter notebook



###############################################################################
# Folder layout (for batch enrolment)          ← informativo, **não** são comandos
###############################################################################
# .
# |-- dataset_faces/
# |   |-- Ana/
# |   |   |-- ana1.jpg
# |   |   `-- ana2.jpg
# |   `-- Carlos/
# |       |-- carlos1.png
# |       `-- carlos2.jpg
# |-- face_registration_recognition.ipynb
# |-- environment.yml
# `-- README.md
#
# (Put images in dataset_faces/<PersonName>/ ; the folder name becomes the label.)

###############################################################################
# Main notebook sections
###############################################################################
# 3 ▸ Batch enrolment            – scans dataset_faces/** and updates encodings.pickle
# 4 ▸ Single-photo enrolment     – adds one image without losing existing data
# 5 ▸ Recognition on image       – detects, labels, and writes recognized*.jpg
# 6 ▸ Real-time recognition      – webcam preview (press “q” to quit)

###############################################################################
# Adding more faces later
###############################################################################
# 1. conda activate facerec
# 2. Run section 4 (or section 3 if you added new folders)
# 3. encodings.pickle grows cumulatively — nothing is overwritten

###############################################################################
# License
###############################################################################
# MIT License — see the LICENSE file


