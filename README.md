# Sistema de Reconhecimento Facial com dlib + CUDA

Este projeto realiza o reconhecimento facial em tempo real utilizando a biblioteca `dlib` com **aceleração por GPU (CUDA)**. Também utiliza `face_recognition`, `OpenCV` e integração com banco de dados MySQL para gerenciar encodings faciais.

## Requisitos do Sistema

### 1. Instale o Cmake 3.26.6

- Versão compatível: cmake-3.26.6-windows-x86_64.msi
- https://cmake.org/files/v3.26/cmake-3.26.6-windows-x86_64.msi

Antes de instalar o projeto, certifique-se de que o sistema possui os seguintes componentes **já instalados**:

### 2. Python

- Versão **3.9** (ou compatível com os pacotes utilizados)

### 3. Visual Studio

- **Visual Studio 2019 (VS16)**  
- Link para download: https://files03.tchspt.com/down/vs_Community2019.exe
- Inclua o componente **MSVC v142 (14.29)** no instalador do Visual Studio em **desenvolvimento de desktop com C++**.

### 4. CUDA Toolkit

- **CUDA 11.8**  
- Baixar em: https://developer.nvidia.com/cuda-11-8-0-download-archive

### 5. cuDNN

- **cuDNN 8.9.7 para CUDA 11.8**  
- Baixar em: https://developer.nvidia.com/rdp/cudnn-archive

Instale o cuDNN copiando os arquivos das pastas (bin, include e lib/x64) para dentro das pastas de instalação do CUDA, em:

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8

- bin
- include
- lib/x64

## Instalação

### 6. Clone o repositório

- git clone https://github.com/seu-usuario/projetc-face-recognition-gpu.git
- cd projetc-face-recognition-gpu

### 7. Crie e ative um ambiente virtual

- python -m venv env
- env\Scripts\activate

### 8. Instale as dependências Python

- pip install -r requirements.txt
- pip install torch==2.2.2+cu118 torchvision==0.17.2+cu118 torchaudio==2.2.2+cu118 --index-url https://download.pytorch.org/whl/cu118


## Compilando o dlib com suporte a CUDA

### 1. Baixe e extraia o `dlib` na raiz do projeto

Use a versão: [dlib-19.24.2](https://github.com/davisking/dlib/releases/tag/v19.24)

### 2. Configure a variável de ambiente do CMake

- mkdir build
- cd build
- cmake .. -G "Visual Studio 16 2019" -A x64 -DDLIB_USE_CUDA=ON -DUSE_AVX_INSTRUCTIONS=ON -DCMAKE_CUDA_FLAGS="--allow-unsupported
- cmake --build . --config Release

### 3. Compile e instale o `dlib`

- cd ..
- set CMAKE_GENERATOR=Visual Studio 16 2019
- python setup.py install

O processo deve detectar o CUDA corretamente e ativar o suporte à GPU.  

Se você ver a mensagem **"DLIB WILL USE CUDA"**, está tudo certo.

## Verificando suporte CUDA

Execute o teste abaixo:

  testeDlibCuda.py

    import dlib

    print("CUDA ativado:", dlib.DLIB_USE_CUDA)
    print("Dispositivos CUDA disponíveis:", dlib.cuda.get_num_devices())


Saída esperada:

- CUDA ativado: True
- Dispositivos CUDA disponíveis: 1

## Execução do sistema

Certifique-se de que o banco de dados está configurado corretamente e a câmera está conectada.

Para iniciar:

- python identify_faces_gpu.py

## Configuração do banco de dados

Crie um arquivo `.env` na raiz com as credenciais do MySQL:

  .env
  
    DB_HOST=localhost
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=nome_do_banco

## Limpeza

**Não apague a pasta `dlib-19.24.2`** se você pretende reinstalar ou recompilar.  

Se já foi instalada com sucesso e não pretende mais recompilar, pode apagar.
