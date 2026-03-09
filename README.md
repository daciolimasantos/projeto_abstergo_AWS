# RELATÓRIO DE IMPLEMENTAÇÃO DE SERVIÇOS AWS

Data: 09/03/2026
Empresa: Abstergo Pharma Industries
Resposável: Dacio Lìma

## Introdução
Este relatório apresenta o processo de implementação de ferramentas na empresa Abstergo Industries, realizado por Dacio Lìma. O objetivo do projeto foi elencar 3 serviços AWS, com a finalidade de realizar a diminuição de custos imediatos, focando principalmente no setor de Pesquisa e Desenvolvimento (P&D) e na modernização do legado de dados da empresa.

## Descrição do Projeto
O projeto de implementação de ferramentas foi dividido em 3 etapas, cada uma com seus objetivos específicos, visando a otimização do fluxo de dados de pesquisas clínicas e a redução da dependência de servidores físicos locais de alto custo.

A seguir, serão descritas as etapas do projeto:

Etapa 1: Amazon S3 (Simple Storage Service) com Ciclo de Vida Inteligente

Nome da Ferramenta: Amazon S3 + S3 Intelligent-Tiering

Foco da Ferramenta: Armazenamento de dados de pesquisa e redução de custos de armazenamento a longo prazo.

Descrição de Utilização:
A Abstergo gera diariamente petabytes de dados de sequenciamento genético e simulações moleculares. Anteriormente, esses dados eram armazenados em fitas LTO (caras e lentas para recuperação) e storages NAS locais de alto custo.
Implementamos o Amazon S3 como a camada primária de armazenamento. Utilizamos a classe de armazenamento S3 Intelligent-Tiering, que move automaticamente os dados entre quatro camadas de acesso (frequente, infrequente, acesso ocasional e arquivo morto) com base na frequência de acesso, sem alterações no aplicativo e sem custos de recuperação. Isso garantiu que dados de projetos concluídos fossem automaticamente arquivados, gerando uma economia imediata de aproximadamente 40% no custo total de armazenamento, mantendo a segurança e a durabilidade dos dados.

Etapa 2: AWS Lambda e Amazon EventBridge

Nome da Ferramenta: AWS Lambda (Computação Serverless) e Amazon EventBridge (Agendador)

Foco da Ferramenta: Processamento de dados e automação de tarefas de backup/processamento.

Descrição de Utilização:
Para processar os dados brutos dos equipamentos de laboratório que chegavam ao S3, era necessário ter servidores EC2 ligados 24/7, muitas vezes ociosos. Para eliminar esse custo fixo, implementamos funções AWS Lambda.
Configuramos o Amazon EventBridge para disparar funções Lambda em horários específicos (ex: toda meia-noite) e também em resposta a eventos (ex: quando um novo arquivo .fasta (genoma) é carregado no S3). A Lambda executa um script Python (usando bibliotecas como boto3 e pandas) que valida os dados, inicia um pipeline de análise e armazena os resultados em um bucket S3 separado. Com isso, pagamos apenas pelo tempo de computação utilizado (em milissegundos), eliminando o custo de servidores ociosos.

Etapa 3: Amazon CloudWatch e AWS Budgets

Nome da Ferramenta: Amazon CloudWatch (Monitoramento) e AWS Budgets (Orçamento/Gerenciamento de Custos)

Foco da Ferramenta: Monitoramento proativo e governança de custos.

Descrição de Utilização:
Com a migração para a nuvem, o controle de gastos é fundamental para garantir que a redução de custos seja real. Implementamos o Amazon CloudWatch para monitorar a utilização de todos os recursos (S3, Lambda) e criar dashboards de desempenho.
Em conjunto, configuramos o AWS Budgets para criar alertas de gastos. Definimos um orçamento mensal para o setor de P&D e configuramos notificações por e-mail (via Amazon SNS - Simple Notification Service) para alertar a equipe de TI e finanças sempre que os gastos atingirem 80% e 100% do orçamento previsto. Isso permite uma ação rápida para investigar picos de uso não planejados, garantindo que a economia esperada seja alcançada sem surpresas na fatura.

## Conclusão
A implementação de ferramentas na empresa Abstergo Industries tem como esperado a redução significativa de custos com infraestrutura de dados e a automação de processos manuais, o que aumentará a eficiência e a produtividade da empresa. A adoção do S3 Intelligent-Tiering reduziu os custos de armazenamento, o AWS Lambda eliminou servidores ociosos e o AWS Budgets trouxe governança financeira. Recomenda-se a continuidade da utilização das ferramentas implementadas e a busca por novas tecnologias que possam melhorar ainda mais os processos da empresa, como a adoção de Amazon SageMaker para criação de modelos preditivos com os dados agora centralizados.

## Anexos


Assinatura do Responsável pelo Projeto:
Dacio Lìma