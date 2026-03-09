#!/usr/bin/env python3
"""
Script para testar a função Lambda localmente
Simula um evento do S3
"""

import json
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from lambda_function import lambda_handler

def criar_evento_teste():
    """
    Cria um evento simulado do S3 para teste
    """
    return {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2026-03-09T12:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "abstergo-dados-brutos-teste",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE"
                        },
                        "arn": "arn:aws:s3:::abstergo-dados-brutos-teste"
                    },
                    "object": {
                        "key": "amostras/2026/03/09/SEQ_001_ABSTERGO_CRISPR_CAS9.fasta",
                        "size": 1024,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0123456789ABCDEF"
                    }
                }
            }
        ]
    }

def main():
    """
    Função principal de teste
    """
    print("=" * 60)
    print("TESTE LOCAL DA FUNÇÃO LAMBDA - ABSTERGO INDUSTRIES")
    print("=" * 60)
    
    # Cria evento de teste
    evento = criar_evento_teste()
    print(f"\n📦 Evento de teste criado:")
    print(f"   Bucket: {evento['Records'][0]['s3']['bucket']['name']}")
    print(f"   Arquivo: {evento['Records'][0]['s3']['object']['key']}")
    
    # Executa a função Lambda
    print(f"\n⚙️  Executando função Lambda...")
    try:
        resultado = lambda_handler(evento, {})
        print(f"\n✅ Execução concluída!")
        print(f"\n📊 Resultado:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        if resultado['statusCode'] == 200:
            print(f"\n🎉 SUCESSO! Processamento realizado com sucesso.")
        else:
            print(f"\n❌ ERRO! Status code: {resultado['statusCode']}")
            
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())