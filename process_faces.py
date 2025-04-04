import os
import face_recognition
import mysql.connector
import numpy as np
from dotenv import load_dotenv
from PIL import Image

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

print("Olá Mundo Final")

# Configurações básicas
diretorio = 'imagens'

DB_NAME = os.getenv('DB_NAME')

def criar_banco_de_dados():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE DATABASE IF NOT EXISTS {DB_NAME}
        DEFAULT CHARACTER SET utf8
        DEFAULT COLLATE utf8_general_ci;
    ''')
    conn.commit()
    conn.close()

def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=DB_NAME  # Usar o nome correto da variável de ambiente
    )

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            encoding LONGBLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Execução
criar_banco_de_dados()
criar_tabela()
print('Banco de dados e tabela criados com sucesso, ou já existiam.')

conn = conectar_banco()
cursor = conn.cursor()

for pasta in os.listdir(diretorio):
    pasta_path = os.path.join(diretorio, pasta)
    if os.path.isdir(pasta_path):
        nome_aluno = pasta
        for filename in os.listdir(pasta_path):
            if filename.lower().endswith(('.jpg', '.png')):
                imagem_path = os.path.join(pasta_path, filename)
                imagem = Image.open(imagem_path)
                imagem = imagem.resize((100, 100))
                imagem = np.array(imagem)

                face_locations = face_recognition.face_locations(imagem, model='cnn')
                encodings = face_recognition.face_encodings(imagem, face_locations, num_jitters=10)

                if len(encodings) > 0:
                    for encoding in encodings:
                        encoding_blob = encoding.tobytes()
                        cursor.execute('''
                            INSERT INTO pessoas (nome, encoding)
                            VALUES (%s, %s)
                        ''', (nome_aluno, encoding_blob))
                        conn.commit()
                        print(f'O encoding da imagem {filename} do aluno {nome_aluno} foi um sucesso.')
                else:
                    print(f'Não foi possível encontrar face na imagem {filename}.')

                # Apagar a imagem após o processamento
                os.remove(imagem_path)
                print(f'Imagem {filename} apagada com sucesso.')

conn.close()
print('Dados salvos com sucesso no banco de dados MySQL.')
