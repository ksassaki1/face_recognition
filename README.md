###############################################################################
# 🧑‍💻 Projeto de Cadastro e Reconhecimento Facial
###############################################################################

Este projeto utiliza técnicas avançadas de **visão computacional** e **processamento de imagens** para cadastrar rostos e realizar reconhecimento facial. As features faciais são extraídas usando embeddings de 128 dimensões pela biblioteca **dlib**, permitindo identificação precisa tanto em fotos estáticas quanto por webcam em tempo real.

---

###############################################################################
# 🎯 Objetivo
###############################################################################

- Desenvolver uma rotina para cadastro facial (batch e individual) usando embeddings faciais.
- Realizar reconhecimento facial preciso e em tempo real em imagens e vídeo por webcam.

---

###############################################################################
# 🛠 Tecnologias e Ferramentas Usadas
###############################################################################

- **Linguagem:** Python
- **Bibliotecas:**
  - `face_recognition` (dlib) – para extração dos embeddings faciais
  - `OpenCV` – processamento e visualização das imagens
  - `NumPy` – manipulação eficiente de dados
  - `Jupyter Notebook` – interface interativa
  - `Conda` – gerenciamento do ambiente de desenvolvimento

---

###############################################################################
# 📂 Estrutura do Projeto (para cadastro em lote) ← informativo, NÃO são comandos
###############################################################################

.
├── dataset_faces/
│   ├── Ana/
│   │   ├── ana1.jpg
│   │   └── ana2.jpg
│   └── Carlos/
│       ├── carlos1.png
│       └── carlos2.jpg
├── face_registration_recognition.ipynb
├── environment.yml
└── README.md

# Nota: Insira imagens em dataset_faces/<NomePessoa>/; o nome da pasta é usado como rótulo.

---

###############################################################################
# 🚀 Quick Start
###############################################################################

# 1 ▸ Clone o repositório
git clone https://github.com/ksassaki1/face_recognition.git
cd face_recognition

# 2 ▸ Crie e ative o ambiente Conda
conda env create -f environment.yml
conda activate facerec

# 3 ▸ Inicie o Jupyter Notebook
jupyter lab      # ou: jupyter notebook

---

###############################################################################
# 📚 Seções Principais do Notebook
###############################################################################

# 3 ▸ Batch enrolment         – cadastra rostos em lote, atualiza encodings.pickle
# 4 ▸ Single-photo enrolment  – adiciona uma imagem sem sobrescrever dados existentes
# 5 ▸ Recognition on image    – reconhece e rotula rostos em imagens estáticas
# 6 ▸ Real-time recognition   – reconhecimento facial em vídeo (pressione "q" para sair)

---

###############################################################################
# ♻️ Adicionando Novos Rostos Depois
###############################################################################

# 1. conda activate facerec
# 2. Execute seção 4 (ou seção 3 caso adicione novas pastas)
# 3. encodings.pickle cresce cumulativamente, sem perda dos dados anteriores

---

###############################################################################
# 📄 Licença
###############################################################################

# MIT License — consulte o arquivo LICENSE
