📊 Pipeline de Inteligência de Mercado: B3 & Cripto
Este projeto é um ecossistema completo de dados que automatiza a coleta, o tratamento e a visualização de ativos financeiros. Ele transforma dados brutos em indicadores estratégicos, utilizando uma arquitetura robusta baseada em contêineres para garantir que o pipeline rode de forma confiável todos os dias.

🛠️ Tecnologias Utilizadas
Linguagem: Python (Pandas, Numpy, SQLAlchemy)

Orquestração: Apache Airflow

Infraestrutura: Docker & Docker Compose

Banco de Dados: PostgreSQL

Visualização: Power BI

🏗️ Arquitetura do Pipeline (ETL)
1. Extração (Data Sourcing)
Captura automatizada de múltiplas fontes para uma visão macro e microeconômica:

Ações (B3): Ativos com as maiores variações via APIs financeiras.

Criptomoedas: Preços e variações das principais moedas em tempo real (BRL).

Dados Macro: Indicadores como Selic, IPCA e taxas de câmbio (Dólar/Euro).

2. Transformação (Feature Engineering & Storytelling)
Aplicação de regras de negócio para gerar insights acionáveis:

Variação Nominal (R$): Criação da coluna variacao_rs para mostrar o impacto financeiro real por cota.

Categorização Inteligente: Uso de np.select para classificar a relevância dos movimentos (ex: Alta Relevante > 3% para B3; Forte Alta > 7% para Cripto).

Sanitização: Padronização de nomes em snake_case e arredondamentos para precisão financeira.

3. Carga e Armazenamento (PostgreSQL)
Os dados tratados são enviados para um banco de dados PostgreSQL rodando em um contêiner Docker.

Persistência: Garantia de histórico para análises temporais.

Conectividade: Estrutura otimizada para consumo via SQL ou integração direta com ferramentas de BI.

⚙️ Orquestração e Automação (Airflow + Docker)
O diferencial técnico deste projeto é a utilização do Apache Airflow para gerenciar o fluxo de dados.

DAGs (Directed Acyclic Graphs): O pipeline é desenhado como uma série de tarefas dependentes (Extrair >> Transformar >> Carregar).

Monitoramento: Interface visual para acompanhar o sucesso das execuções e logs de erro em tempo real.

Dockerized: Todo o ambiente (Airflow, Postgres, Redis) é orquestrado via Docker Compose, permitindo que o projeto seja replicado em qualquer servidor com apenas um comando.

📈 Visualização: Dashboard Power BI
Para encerrar o ciclo do dado, desenvolvi um dashboard no Power BI conectado diretamente ao PostgreSQL.

Foco: Data Storytelling.

Diferencial: O dashboard não mostra apenas "o que aconteceu", mas sim o "que fazer agora" através de alertas de status de mercado e tendências filtradas por relevância.

🚀 Como Executar
Certifique-se de ter o Docker instalado.

Clone o repositório.

No terminal, execute:

Bash
docker compose up -d
Acesse o Airflow em localhost:8080 para acompanhar o pipeline.