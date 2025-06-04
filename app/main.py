import os
import io
import pickle
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from PIL import Image
import face_recognition

app = FastAPI()

# ──────────── Configurações ────────────

# Guarda embeddings e nomes em memória
KNOWN_ENCODINGS = []
KNOWN_NAMES = []

# Se quisermos persistir encodings para que não se percam ao reiniciar:
ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), "encodings.pickle")

# Diretório de “known_faces” (onde pastas manuais ou do register vão parar)
KNOWN_FACES_DIR = os.path.join(os.path.dirname(__file__), "known_faces")
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

# ──────────── Funções auxiliares ────────────

def load_encodings_from_disk():
    """
    Se existir um encodings.pickle, carrega listas: names e encodings.
    """
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
            return data.get("names", []), data.get("encodings", [])
    return [], []

def save_encodings_to_disk(names, encodings):
    """
    Persiste em disco o dicionário {"names": [...], "encodings": [...]}.
    """
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump({"names": names, "encodings": encodings}, f)

def load_known_faces_from_folders():
    """
    Varre todo KNOWN_FACES_DIR/<NomePessoa> e extrai embeddings.
    Popula KNOWN_ENCODINGS e KNOWN_NAMES (listas globais).
    """
    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue
        for filename in os.listdir(person_dir):
            filepath = os.path.join(person_dir, filename)
            try:
                img = face_recognition.load_image_file(filepath)
                encs = face_recognition.face_encodings(img)
                if encs:
                    KNOWN_ENCODINGS.append(encs[0])
                    KNOWN_NAMES.append(person_name)
            except Exception:
                # se der erro em alguma imagem, ignora e segue
                pass

@app.on_event("startup")
def startup_event():
    """
    1) Se existirem encodings salvos em disco (pickle), carrega primeiro.
    2) Depois varre a pasta known_faces para pegar qualquer imagem nova.
    """
    # 1) Carrega do arquivo, se existir
    names_on_disk, encs_on_disk = load_encodings_from_disk()
    KNOWN_NAMES.extend(names_on_disk)
    KNOWN_ENCODINGS.extend(encs_on_disk)

    # 2) Carrega imagens que estejam em app/known_faces/ (se ainda não estiverem na lista)
    load_known_faces_from_folders()

# ──────────── Endpoints HTML ────────────

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Página HTML com dois formulários:
    - /register (cadastra nova pessoa)
    - /recognize (reconhece quem está na foto)
    """
    return """
    <html>
      <head>
        <title>Face Recognition API</title>
      </head>
      <body>
        <h2>Cadastro de nova pessoa</h2>
        <form action="/register" enctype="multipart/form-data" method="post">
          <label>Nome:</label>
          <input type="text" name="name" required/>
          <br/><br/>
          <label>Imagem (.jpg, .png):</label>
          <input type="file" name="file" accept="image/*" required/>
          <br/><br/>
          <input type="submit" value="Cadastrar"/>
        </form>

        <hr/>

        <h2>Reconhecimento facial</h2>
        <form action="/recognize" enctype="multipart/form-data" method="post">
          <label>Arquivo de imagem:</label>
          <input type="file" name="file" accept="image/*" required/>
          <br/><br/>
          <input type="submit" value="Reconhecer"/>
        </form>
      </body>
    </html>
    """

# ──────────── Endpoint de cadastro ────────────

@app.post("/register")
async def register_face(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Recebe um nome + uma imagem contendo exatamente 1 rosto.
    1) Valida tipo de arquivo (image/*)
    2) Extrai embedding
    3) Salva a imagem em app/known_faces/<name>/
    4) Adiciona (name, embedding) nas listas em memória
    5) Persiste embeddings em encodings.pickle
    """
    # 1) Verifica se é imagem
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")

    # 2) Lê conteúdo e extrai embedding
    contents = await file.read()
    img = face_recognition.load_image_file(io.BytesIO(contents))
    encs = face_recognition.face_encodings(img)

    if len(encs) == 0:
        return JSONResponse(status_code=400, content={"detail": "Nenhum rosto encontrado na imagem"})
    if len(encs) > 1:
        return JSONResponse(status_code=400, content={"detail": "Mais de um rosto detectado; envie apenas uma foto por vez"})

    embedding = encs[0]

    # 3) Salva a imagem bruta em app/known_faces/<name>/
    person_folder = os.path.join(KNOWN_FACES_DIR, name)
    os.makedirs(person_folder, exist_ok=True)
    # Acha extensão (pode ser .jpg, .jpeg, .png …)
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        ext = ".jpg"
    # Cria nome único (timestamp)
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name.replace(' ', '_')}_{ts}{ext}"
    filepath = os.path.join(person_folder, filename)
    with open(filepath, "wb") as f_img:
        f_img.write(contents)

    # 4) Atualiza listas em memória
    KNOWN_NAMES.append(name)
    KNOWN_ENCODINGS.append(embedding)

    # 5) Persiste em disco (encodings.pickle)
    save_encodings_to_disk(KNOWN_NAMES, KNOWN_ENCODINGS)

    return {"detail": f"Rosto de '{name}' cadastrado com sucesso"}

# ──────────── Endpoint de reconhecimento ────────────

@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """
    Recebe apenas uma imagem (pode conter 0, 1 ou mais rostos).
    Se não encontrar rostos, retorna “No face found”.
    Se encontrar, compara com KNOWN_ENCODINGS e retorna o nome (ou “Unknown”).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")

    contents = await file.read()
    img = face_recognition.load_image_file(io.BytesIO(contents))
    encs = face_recognition.face_encodings(img)

    if not encs:
        return JSONResponse(status_code=200, content={"name": "No face found"})

    embedding = encs[0]

    if not KNOWN_ENCODINGS:
        return JSONResponse(status_code=200, content={"name": "Unknown"})

    distances = face_recognition.face_distance(KNOWN_ENCODINGS, embedding)
    best_index = np.argmin(distances)
    if distances[best_index] < 0.6:
        return JSONResponse(status_code=200, content={"name": KNOWN_NAMES[best_index]})
    else:
        return JSONResponse(status_code=200, content={"name": "Unknown"})
