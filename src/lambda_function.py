#código não produtivo - apenas para fins de estudos e entrega do projeto.

import json
import boto3
import pandas as pd
import logging
from datetime import datetime
import os

# Configuração de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialização dos clientes AWS
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Tabela para registrar o processamento (criar no DynamoDB posteriormente)
table = dynamodb.Table('ProcessamentoGenomico')

def lambda_handler(event, context):
    """
    Função Lambda para processar dados genômicos da Abstergo Industries
    Disparada quando novos arquivos .fasta são carregados no S3
    """
    
    logger.info(f"Evento recebido: {json.dumps(event)}")
    
    try:
        # Obtém informações do arquivo que disparou o evento
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        
        logger.info(f"Processando arquivo: {file_key} do bucket: {bucket_name}")
        
        # Baixa o arquivo do S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Simula processamento de dados genômicos
        resultado_processamento = processar_dados_genomicos(file_content, file_key)
        
        # Salva resultados em um bucket de resultados
        bucket_resultado = 'abstergo-dados-processados'
        resultado_key = f"resultados/{datetime.now().strftime('%Y/%m/%d')}/resultado_{file_key}.json"
        
        s3_client.put_object(
            Bucket=bucket_resultado,
            Key=resultado_key,
            Body=json.dumps(resultado_processamento, indent=2),
            ContentType='application/json'
        )
        
        # Registra o processamento no DynamoDB
        table.put_item(
            Item={
                'arquivo_id': file_key.replace('/', '_'),
                'timestamp': datetime.now().isoformat(),
                'bucket_origem': bucket_name,
                'bucket_resultado': bucket_resultado,
                'status': 'SUCESSO',
                'sequencias_encontradas': resultado_processamento['sequencias_validas'],
                'tempo_processamento_ms': resultado_processamento['tempo_processamento_ms']
            }
        )
        
        logger.info(f"Arquivo {file_key} processado com sucesso!")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processamento concluído com sucesso',
                'arquivo': file_key,
                'resultado': resultado_key
            })
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        
        # Registra erro no DynamoDB
        table.put_item(
            Item={
                'arquivo_id': file_key.replace('/', '_') if 'file_key' in locals() else 'erro_desconhecido',
                'timestamp': datetime.now().isoformat(),
                'status': 'ERRO',
                'mensagem_erro': str(e)
            }
        )
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro no processamento',
                'error': str(e)
            })
        }

def processar_dados_genomicos(conteudo, nome_arquivo):
    """
    Simula o processamento de dados genômicos
    Em um cenário real, isso seria um pipeline complexo de bioinformática
    """
    import time
    import random
    
    inicio = time.time()
    
    # Simula processamento pesado
    time.sleep(1.5)  # 1.5 segundos de processamento
    
    # Dados fictícios do processamento
    resultado = {
        'nome_arquivo': nome_arquivo,
        'data_processamento': datetime.now().isoformat(),
        'sequencias_validas': random.randint(1500, 3000),
        'sequencias_invalidas': random.randint(5, 50),
        'comprimento_medio_sequencias': random.randint(500, 2000),
        'gc_content_percentual': round(random.uniform(35.0, 65.0), 2),
        'qualidade_media_phred': round(random.uniform(30.0, 40.0), 2),
        'variantes_geneticas_encontradas': random.randint(10, 100),
        'tempo_processamento_ms': round((time.time() - inicio) * 1000, 2),
        'versao_pipeline': '2.3.1',
        'responsavel_processamento': 'Dacio Lima'
    }
    
    return resultado