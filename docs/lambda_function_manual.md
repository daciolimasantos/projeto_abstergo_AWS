# Lambda Function Manual

---

## 🚀 Introdução

A partir daqui vamso explicar o passo a passo desse código, para que seja de fácil compreensão e aprendizado inclusive do criador do código.

Vamos abrir esse manual e ler cada parte, como se estivéssemos montando um robô que trabalha em um armazém e faz de certa forma a logísitica. Prepare-se!

---

## 🛠️ Parte 1: Pegando as Ferramentas (Imports)

Primeiro, o robô precisa saber quais ferramentas ele tem na caixa.

```python
import json
import boto3
import pandas as pd
import logging
from datetime import datetime
import os
```

*   **O que é:** São comandos `import`. O `import` é a função em Python para utilizar funções já existentes de outros bibliotecas.
    * por exmeplo: ao invés de criar uma função de faça soma, multiplicação, subtração e afins, você pode importar uma biblioteca que já possui todas essas fórmulas como função.
    * então você não precisa saber necessariamente fazer a conta, pois a biblioteca já tem isso dentro dela.

*   **O que faz:** Então pensa como se você estivesse abrindo a caixa de ferramentas e pegando:
    *   `json`: Uma caixa de mensagens para conversar com o computador.
    *   `boto3`: O **controle remoto** para falar com a AWS (a nuvem).
    *   `pandas`: Uma calculadora superpoderosa para dados.
    *   `logging`: Um **diário** para o robô anotar o que ele faz.
    *   `datetime`: Um relógio para saber a hora.
    *   `os`: Ferramentas para mexer com pastas do computador. `os` significa (operational system/sistema operacional)
*   **Por que:** Sem essas ferramentas, o robô não saberia como ler arquivos, nem como guardar informações, nem como saber a hora.

---

## 📝 Parte 2: Preparando o Diário e o Caderno (Configuração)

Agora o robô se prepara para trabalhar.

```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```
*   **O que faz:** Cria o "Diário do Robô" e diz: "Anote tudo que for importante (INFO)".
*   **Por que:** Se algo der errado, o robô precisa saber o que aconteceu para não ficar confuso e ter uma base para encontrar o erro, ou os erros.

```python
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
```
*   **O que faz:**
    *   `s3_client`: Conecta o robô ao **Armazém de Arquivos** (S3). aqui o robô vai acessar o meu computador no disco C:, onde tem la seus documentos e downloads.
    *   `dynamodb`: Conecta o robô ao **Caderno de Anotações** (DynamoDB). `dynamobd` é um serviço de banco de dados, assim como o postgresql, mysql et.
    *   para leigos pense nele como um worbook do excel com inifinidade de worksheets.
*   **Por que:** O robô precisa de um endereço para buscar os arquivos e um caderno para anotar o trabalho feito.

```python
table = dynamodb.Table('ProcessamentoGenomico')
```
*   **O que faz:** Abre uma página específica no caderno chamada "ProcessamentoGenomico".
*   **Por que:** Para não misturar as anotações de DNA com as anotações de outras coisas.

---

## 🧠 Parte 3: O Cérebro do Robô (Função `lambda_handler`)

Esta é a parte mais importante! É a função principal que acorda quando alguém coloca um arquivo novo.

```python
def lambda_handler(event, context):
    """
    Função Lambda para processar dados genômicos da Abstergo Industries
    Disparada quando novos arquivos .fasta são carregados no S3
    """
```
*   **O que faz:** Define o nome da função (`lambda_handler`).
*   **Por que:** O nome `lambda_handler` é o padrão para dizer "Eu sou o robô que trabalha na nuvem". O texto entre as aspas (`"""`) é uma nota para humanos entenderem o que o robô faz.

```python
    logger.info(f"Evento recebido: {json.dumps(event)}")
```
*   **O que faz:** O robô olha para o "Evento" (a campainha que tocou) e anota no diário o que aconteceu.
*   **Por que:** Para saber quem mandou o arquivo e quando. Pense nele como um guarda na cancela de um prédio.

```python
    try:
        # Obtém informações do arquivo que disparou o evento
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
```
*   **O que faz:** O robô lê a mensagem e descobre:
    *   `bucket_name`: Qual armazém o arquivo veio?
    *   `file_key`: Qual é o nome do arquivo?
*   **Por que:** O robô precisa saber **onde** procurar o arquivo para poder pegá-lo.

```python
        logger.info(f"Processando arquivo: {file_key} do bucket: {bucket_name}")
```
*   **O que faz:** Anota no diário: "Vou processar o arquivo XPTO agora".
*   **Por que:** Para ter certeza de que ele está trabalhando no arquivo certo.

```python
        # Baixa o arquivo do S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
```
*   **O que faz:** O robô vai até o armazém, pega o arquivo e lê o conteúdo dele.
*   **Por que:** O robô não pode analisar o arquivo se ele estiver trancado no armazém. Ele precisa trazer para a "mão" dele.

```python
        # Simula processamento de dados genômicos
        resultado_processamento = processar_dados_genomicos(file_content, file_key)
```
*   **O que faz:** Chama uma função auxiliar (que vamos ver depois) para fazer a mágica acontecer.
*   **Por que:** Para não poluir o cérebro principal com muitos detalhes. É como pedir ajuda para um especialista.

```python
        # Salva resultados em um bucket de resultados
        bucket_resultado = 'abstergo-dados-processados'
        resultado_key = f"resultados/{datetime.now().strftime('%Y/%m/%d')}/resultado_{file_key}.json"
```
*   **O que faz:** Define onde o resultado vai ficar e cria um nome para o arquivo de resultado (com a data de hoje).
*   **Por que:** Para organizar os resultados em pastas por data, assim não fica bagunçado.

```python
        s3_client.put_object(
            Bucket=bucket_resultado,
            Key=resultado_key,
            Body=json.dumps(resultado_processamento, indent=2),
            ContentType='application/json'
        )
```
*   **O que faz:** Guarda o resultado no armazém de resultados.
*   **Por que:** Para que os cientistas possam baixar o relatório depois.

```python
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
```
*   **O que faz:** Escreve no caderno de anotações (DynamoDB) que tudo deu certo.
*   **Por que:** Para criar um histórico. Se alguém perguntar "O arquivo X foi processado?", o robô pode olhar o caderno e responder.

```python
        logger.info(f"Arquivo {file_key} processado com sucesso!")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processamento concluído com sucesso',
                'arquivo': file_key,
                'resultado': resultado_key
            })
        }
```
*   **O que faz:** O robô avisa que terminou e manda uma mensagem de "Tudo OK" (código 200).
*   **Por que:** Para quem enviou o arquivo saber que pode ir dormir tranquilo.

---

## 🛡️ Parte 4: O Plano de Segurança (O que dá errado?)

Nada é perfeito. Às vezes o robô pode tropeçar.

```python
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
```
*   **O que faz:** Se algo der errado (o `try` falhar), ele vai para o `except`. Anota o erro no diário.
*   **Por que:** Para saber qual foi o problema.

```python
        # Registra erro no DynamoDB
        table.put_item(
            Item={
                'arquivo_id': file_key.replace('/', '_') if 'file_key' in locals() else 'erro_desconhecido',
                'timestamp': datetime.now().isoformat(),
                'status': 'ERRO',
                'mensagem_erro': str(e)
            }
        )
```
*   **O que faz:** Anota no caderno que deu **ERRO**. Se ele souber o nome do arquivo, anota o nome. Se não souber, anota "erro_desconhecido".
*   **Por que:** Para que os humanos saibam qual arquivo quebrou o robô.

```python
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro no processamento',
                'error': str(e)
            })
        }
```
*   **O que faz:** Manda uma mensagem de "Shiii, deu ruim" (código 500).
*   **Por que:** Para avisar que o trabalho não foi concluído.

---

## 🤖 Parte 5: O Especialista (Função `processar_dados_genomicos`)

Agora vamos ver o que o robô faz quando pede ajuda.

```python
def processar_dados_genomicos(conteudo, nome_arquivo):
    """
    Simula o processamento de dados genômicos
    Em um cenário real, isso seria um pipeline complexo de bioinformática
    """
```
*   **O que faz:** Cria uma função que recebe o texto do arquivo e o nome dele.
*   **Por que:** Para separar a lógica de "analisar DNA" do resto do código.

```python
    import time
    import random
    
    inicio = time.time()
    
    # Simula processamento pesado
    time.sleep(1.5)  # 1.5 segundos de processamento
```
*   **O que faz:** Pega a hora atual e faz o robô "dormir" por 1.5 segundos.
*   **Por que:** É uma **simulação**. Na vida real, analisar DNA demora muito. Aqui, só estamos fingindo que está pensando para o código não ser instantâneo demais.

```python
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
```
*   **O que faz:** Cria um "boletim" com números aleatórios.
*   **Por que:** Como é um exemplo, não temos DNA real. Usamos números aleatórios (`random`) para parecer que o robô encontrou coisas. O `time.time() - inicio` calcula quanto tempo o robô demorou.

```python
    return resultado
```
*   **O que faz:** Entrega o boletim para o cérebro principal.
*   **Por que:** Para que o cérebro possa guardar esse resultado no armazém.

---

## 🎓 Resumo


1.  **Automação:** O código faz o trabalho chato de mover arquivos e anotar dados sem você precisar apertar botões.
2.  **Organização:** Usamos o **S3** para guardar arquivos e o **DynamoDB** para guardar informações sobre esses arquivos.
3.  **Segurança:** O `try/except` garante que, se algo quebrar, o robô não morre, ele apenas anota o erro e avisa.
4.  **Simulação:** Às vezes, no começo, usamos dados falsos para testar se o robô funciona antes de colocar dados reais.

Esse código é a base de como grandes empresas (como a Abstergo, que é fictícia, mas lembra a tecnologia real) processam milhões de dados de DNA todos os dias!

Você entendeu como o robô funciona? Se tiver mais dúvidas, é só chamar! 🧬💻

***