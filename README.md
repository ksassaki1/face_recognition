# 🧑‍💻 **Projeto de Cadastro e Reconhecimento Facial com API e Docker**

Este projeto utiliza técnicas avançadas de **processamento de imagens** e **visão computacional** para realizar o **cadastro e reconhecimento facial**. As faces são cadastradas através da extração de embeddings faciais de **128 dimensões** utilizando a biblioteca **dlib** (por meio do wrapper `face_recognition`). O sistema disponibiliza:

- **Cadastro de rostos** via:
  1. Pastas locais (`app/known_faces/<NomePessoa>/`), carregadas no startup.  
  2. Formulário no navegador (`/register`).  
  3. Script em Jupyter Notebook (`facerec_api.ipynb`).  

- **Reconhecimento facial** em:
  - Imagens estáticas (upload via navegador, curl ou notebook).   

Tudo está containerizado em **Docker**, facilitando a implantação em qualquer máquina.

---

## 🎯 **Objetivo**
- Construir um microserviço em **FastAPI** que permita:
  - **Cadastrar** novos rostos dinamicamente (nome + imagem) via API.  
  - **Reconhecer** quem aparece em uma imagem, retornando o nome ou “Unknown”.  
- Demonstrar consumo da API em um **Jupyter Notebook**, integrando cadastro e reconhecimento de ponta a ponta.  
- Containerizar tudo com **Docker**, expondo uma interface web simples para upload.

---

## 🛠 **Tecnologias e Ferramentas Usadas**
- **Linguagem:** Python 3.10  
- **Framework de API:** FastAPI (+ Uvicorn)  
- **Bibliotecas Python:**
  - `face_recognition`: Extração e comparação de embeddings faciais.  
  - `dlib`: Modelo de embeddings faciais 128D (via `face_recognition`).  
  - `numpy`: Operações numéricas e cálculos de distância.  
  - `python-multipart`: Suporte a upload de arquivos via FastAPI.  
  - `pillow`: Carregamento/visualização de imagens em notebook e API.  
- **Notebook Interativo:** Jupyter Notebook (`facerec_api.ipynb`)  
  - Demonstra cadastro e reconhecimento via chamadas HTTP.  
- **Containerização:** Docker  
- **Frontend Mínimo:** Formulários HTML gerados por FastAPI em `/` (dois formulários: cadastro e reconhecimento).

---

## 📂 **Estrutura do Projeto**
### **Arquivos e Diretórios**
- **`app/main.py`**: Aplicação FastAPI com endpoints:
  - **GET /**: retorna página HTML com formulários para cadastro (`/register`) e reconhecimento (`/recognize`).
  - **POST /register**: recebe `name` e `file`, extrai embedding, salva imagem em `app/known_faces/<name>/`, atualiza listas em memória e persiste em `encodings.pickle`.
  - **POST /recognize**: recebe `file`, extrai embedding da primeira face e compara com embeddings cadastrados, retornando `{ "name": "<Pessoa>" }`, `"Unknown"` ou `"No face found"`.

- **`app/known_faces/`**: Pasta onde se acumulam subpastas `<NomePessoa>/` contendo as imagens de referência.  
  - No startup, o servidor varre esse diretório e carrega todos os embeddings.

- **`notebooks/facerec_api.ipynb`**: Notebook Jupyter que exemplifica como:
  1. Registrar novas pessoas chamando `POST /register`.  
  2. Reconhecer rostos chamando `POST /recognize`.  
  3. Exibir imagens de cadastro e de teste, imprimindo as respostas JSON.  
  - Contém funções `register_person(name, image_path)` e `recognize_person(image_path)` usando a biblioteca `requests`.

- **`notebooks/test_images/`**:  
  - Contém imagens de exemplo para demonstração no notebook:
    - `pessoaA_cadastro.jpg`  
    - `pessoaA_teste.jpg`  
    - `unknown_teste.jpg`

- **`requirements.txt`**  
  ```
  fastapi
  uvicorn[standard]
  face_recognition
  python-multipart
  pillow
  numpy
  ```

* **`Dockerfile`**:

  * Base: `python:3.10-slim`.
  * Instala via `apt` dependências de sistema necessárias para compilar o `dlib` e bibliotecas de imagem.
  * Cria a pasta `app/known_faces/`.
  * Copia `requirements.txt` e instala dependências Python.
  * Copia todo o diretório `app/` (incluindo `main.py` e `known_faces/`).
  * Expõe a porta `8005` e inicia Uvicorn em `--port 8005`.

```
facerecognition/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── known_faces/
│       └── (subpastas vazias ou com fotos pré-existentes)
│
├── notebooks/
│   ├── test_images/
│   │   ├── pessoaA_cadastro.jpg
│   │   ├── pessoaA_teste.jpg
│   │   └── unknown_teste.jpg
│   └── facerec_api.ipynb
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 **Como Rodar com Docker**

1. **Build da imagem**
   Na raiz do repositório (onde está o `Dockerfile`), execute:

   ```bash
   docker build -t facerec-api .
   ```

   Isso cria a imagem `facerec-api` com todas as bibliotecas instaladas.

2. **Subir o container**

   ```bash
   docker run -d --name facerec-api-container -p 8005:8005 facerec-api
   ```

   * `-d`: roda em modo detached (background).
   * `--name`: nomeia o container como `facerec-api-container`.
   * `-p 8005:8005`: mapeia a porta `8005` do host para a mesma porta dentro do container (onde Uvicorn escuta).

3. **Verificar se está rodando**

   ```bash
   docker ps
   ```

   Saída esperada:

   ```
   CONTAINER ID   IMAGE         COMMAND                        STATUS         PORTS                    NAMES
   abcdef123456   facerec-api   "python -m uvicorn app.m…"     Up X seconds   0.0.0.0:8005->8005/tcp   facerec-api-container
   ```

4. **Testar no navegador**

   * Abra `http://localhost:8005/`: aparecerá a página com dois formulários.
   * Abra `http://localhost:8005/docs`: interface Swagger gerada automaticamente.

---

## 📝 **Uso da Interface Web (formulários HTML)**

1. **Página inicial (`/`)**

   * Exibe dois formulários:

     1. **Cadastro de nova pessoa**

        * Campo **Nome** (input text).
        * Campo **Imagem** (input file).
        * Botão **Cadastrar**.
        * Envia para `POST /register`.
     2. **Reconhecimento facial**

        * Campo **Imagem** (input file).
        * Botão **Reconhecer**.
        * Envia para `POST /recognize`.

2. **Cadastro via formulário**

   * Preencha **Nome** com o rótulo desejado (ex.: “PessoaA”).
   * Selecione a imagem contendo apenas 1 rosto (jpg, png).
   * Clique em **Cadastrar**.
   * Se bem-sucedido, a resposta JSON exibirá:

     ```json
     { "detail": "Rosto de 'PessoaA' cadastrado com sucesso" }
     ```

3. **Reconhecimento via formulário**

   * Selecione uma imagem de teste.
   * Clique em **Reconhecer**.
   * Abaixo do formulário aparecerá o JSON:

     ```json
     { "name": "PessoaA" }
     ```

     ou

     ```json
     { "name": "Unknown" }
     ```

     ou

     ```json
     { "name": "No face found" }
     ```

---

## 📊 **Uso no Jupyter Notebook (`facerec_api.ipynb`)**

1. **Instale dependências (se rodar fora do Docker)**

   ```bash
   pip install requests pillow matplotlib
   ```

2. **Defina a URL base**
   No topo do notebook, ajuste:

   ```python
   BASE_URL = "http://localhost:8005"
   ```

3. **Funções de auxílio**

   * `register_person(name: str, image_path: str)`: faz `POST /register` e retorna o JSON.
   * `recognize_person(image_path: str)`: faz `POST /recognize` e retorna o JSON.

4. **Exemplo de fluxo**

   ```python
   from PIL import Image
   import matplotlib.pyplot as plt

   # 1) Mostrar e cadastrar PessoaA
   path_to_register = "notebooks/test_images/pessoaA_cadastro.jpg"
   img = Image.open(path_to_register)
   plt.imshow(img); plt.axis("off")
   resp_reg = register_person("PessoaA", path_to_register)
   print("Resposta do /register:", resp_reg)

   # 2) Mostrar e reconhecer PessoaA
   path_to_test = "notebooks/test_images/pessoaA_teste.jpg"
   img2 = Image.open(path_to_test)
   plt.figure(); plt.imshow(img2); plt.axis("off")
   resp_rec = recognize_person(path_to_test)
   print("Resposta do /recognize:", resp_rec)

   # 3) Tentar reconhecer uma face não cadastrada
   path_to_unknown = "notebooks/test_images/unknown_teste.jpg"
   img3 = Image.open(path_to_unknown)
   plt.figure(); plt.imshow(img3); plt.axis("off")
   resp_unknown = recognize_person(path_to_unknown)
   print("Resposta do /recognize:", resp_unknown)
   ```

5. **Saída esperada**

   * Cadastro:

     ```json
     { "detail": "Rosto de 'PessoaA' cadastrado com sucesso" }
     ```
   * Reconhecimento (mesmo rosto):

     ```json
     { "name": "PessoaA" }
     ```
   * Reconhecimento (rosto não cadastrado):

     ```json
     { "name": "Unknown" }
     ```

---

## 🔧 **Ambientes de Cadastro**

* **Via pasta (estático)**

  * Se preferir não usar o formulário, basta criar manualmente subpastas em `app/known_faces/<NomePessoa>/` com fotos dentro.
  * Reinicie o container para que o `startup_event` recarregue esses embeddings.

* **Via formulário (/register)**

  * Envia nome + imagem por HTTP sem precisar criar pastas manualmente.
  * Atualiza listas em memória e salva `encodings.pickle` para persistência.

---

## ✅ **Próximos Passos Sugeridos**

* **Persistir encodings fora do container**: monte um volume para `app/` ou insira um DB (SQLite, Redis) para que, ao atualizar o container, mantenha os cadastros.
* **Interface gráfica mais completa**: usar **Streamlit** ou **React** para exibir galeria de rostos cadastrados, status de reconhecimento e estatísticas.
* **Reconhecimento em vídeo real**: adicionar um endpoint que receba stream de vídeo (usando WebSockets ou multipart MJPEG) e responda em tempo real.
* **Validação de imagem**: restringir tamanho máximo, proporções, verificar apenas rostos frontais, etc.
* **Autenticação/Autorização**: proteger endpoints de cadastro para que apenas usuários autorizados possam adicionar novos rostos.

---

## 👤 **Autor**

Guilherme Koiti Tanaka Sassaki
[LinkedIn](https://www.linkedin.com/in/guilherme-sassaki-10b81ba7/)


