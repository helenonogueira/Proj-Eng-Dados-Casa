import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import boto3
import io
import os
import logging


# configuração dos logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def csv_to_minio_etl(bucket_name, endpoint_url, access_key, secret_key):

    # Configuração do cliente MinIO
    minio_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    try:
        df = pd.read_parquet('acidentes_2024.parquet')
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False)
        parquet_buffer.seek(0)
        minio_client.put_object(Bucket=bucket_name, Key='acidentes_2024/data.parquet', Body=parquet_buffer.getvalue())
        logging.info("Arquivo Parquet enviado para o MInIO com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar o arquivo Parquet para o MinIO: {e}")
        raise

# Carregar o CSV e Transformar em Parquet
def carregar_e_salvar_como_parquet(caminho_arquivo_csv, caminho_arquivo_parquet):
    df = pd.read_csv(caminho_arquivo_csv, encoding='latin1')
    df.to_parquet(caminho_arquivo_parquet)

caminho_arquivo_csv = 'C:/Users/Heleno/Documents/EngenhariaDeDados/Projeto_um_pc/acidentes_2024.csv'
caminho_arquivo_parquet = 'C:/Users/Heleno/Documents/EngenhariaDeDados/Projeto_um_pc/acidentes_2024.parquet'
carregar_e_salvar_como_parquet(caminho_arquivo_csv, caminho_arquivo_parquet)

# escrever no minio em .parquet - na bucket landing

bucket_name = "landing"
endpoint_url = "http://localhost:9000"  # Substitua pelo seu endpoint do MinIO
access_key = "minioadmin"
secret_key = "minio@1234!"

csv_to_minio_etl(bucket_name, endpoint_url, access_key, secret_key)