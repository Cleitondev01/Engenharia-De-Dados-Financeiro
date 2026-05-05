# 📊 Pipeline de Inteligência de Mercado: B3 & Cripto

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-3.2.1-017CEE?logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)

> Pipeline ETL completo que coleta, trata e visualiza dados financeiros em tempo real — ações da B3, criptomoedas e indicadores macroeconômicos — com orquestração automática via Apache Airflow e infraestrutura containerizada com Docker.

---

## 📸 Preview

### Dashboard Power BI


<img width="1437" height="807" alt="WhatsApp Image 2026-05-04 at 22 27 22" src="https://github.com/user-attachments/assets/e203ab22-4010-4863-bbb9-d06fb07c2392" />



### Arquitetura do Sistema

<img width="842" height="316" alt="Untitled-2026-04-29-2117BRANCO" src="https://github.com/user-attachments/assets/ded9304c-dd3d-4629-8ac6-824a351cf608" />

---

## 🗂️ Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Arquitetura do Pipeline](#arquitetura-do-pipeline)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Como Executar](#como-executar)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Pipeline em Ação](#pipeline-em-ação)
- [Próximos Passos](#próximos-passos)

---

## 📌 Sobre o Projeto

Este projeto nasceu da vontade de unir duas áreas de interesse: **mercado financeiro** e **engenharia de dados**. O objetivo foi construir um ecossistema completo — da coleta bruta até o dashboard final — sem depender de ferramentas prontas que escondem a complexidade do processo.

O pipeline roda automaticamente todos os dias, captura dados de múltiplas fontes, aplica regras de negócio para gerar indicadores relevantes e disponibiliza tudo em um banco relacional pronto para consumo via BI.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11 (Pandas, NumPy, SQLAlchemy) |
| Extração | yfinance, requests |
| Orquestração | Apache Airflow 2.x |
| Infraestrutura | Docker & Docker Compose |
| Banco de Dados | PostgreSQL 16 |
| Armazenamento Intermediário | Parquet |
| Visualização | Power BI (com HTML/CSS customizado) |

---

## 🏗️ Arquitetura do Pipeline

```
yfinance API
     │
     ▼
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐     ┌──────────┐
│   EXTRACT   │────▶│    TRANSFORM     │────▶│    LOAD     │────▶│ Power BI │
│  (Python)   │     │ (Pandas/NumPy)   │     │ (PostgreSQL)│     │Dashboard │
└─────────────┘     └──────────────────┘     └─────────────┘     └──────────┘
        │                    │
        ▼                    ▼
   Parquet (raw)      Feature Engineering
                      Categorização
                      Sanitização
```

Toda a orquestração é gerenciada pelo **Apache Airflow** via DAGs, e o ambiente completo roda em containers **Docker**.

### 1. Extração

Captura automatizada de múltiplas fontes:

- **Ações (B3):** ativos com as maiores variações do dia via yfinance
- **Criptomoedas:** preços e variações das principais moedas em BRL
- **Dados Macro:** Selic, IPCA, câmbio (Dólar, Euro, Yuan)

### 2. Transformação

Aplicação de regras de negócio para gerar indicadores acionáveis:

- **Variação Nominal (R$):** coluna `variacao_rs` para mostrar o impacto financeiro real por cota
- **Categorização inteligente:** `np.select` classifica a relevância dos movimentos
  - B3: `Alta Relevante` (> 3%), `Alta Moderada` (1–3%), `Estável`, etc.
  - Cripto: `Forte Alta` (> 7%), `Alta` (3–7%), etc.
- **Sanitização:** nomes padronizados em `snake_case`, arredondamentos para precisão financeira

### 3. Carga (PostgreSQL)

- Dados persistidos em tabelas relacionais para histórico e análise temporal
- Estrutura otimizada para consumo direto via SQL ou integração com ferramentas de BI

---

## 📁 Estrutura de Pastas

```
FINANCE_ETL/
├── arq_processados/      # Arquivos Parquet gerados pelo pipeline
├── config/               # Configurações de conexão e variáveis
├── dags/                 # DAGs do Apache Airflow
│   └── finance_dag.py
├── logs/                 # Logs de execução do Airflow
├── plugins/              # Plugins customizados do Airflow
├── docs/                 # Imagens para documentação
│   ├── dashboard.jpeg
│   ├── arquitetura.png
│   ├── airflow.png
│   └── postgres.png
├── .env                  # Variáveis de ambiente (não versionado)
├── docker-compose.yaml   # Orquestração dos containers
├── financas.pbix         # Arquivo do dashboard Power BI
├── main.py               # Script principal do pipeline
├── requirements.txt      # Dependências Python
└── README.md
```

---

## ⚙️ Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/) >= 24.x
- [Docker Compose](https://docs.docker.com/compose/) >= 2.x
- Git

> **Não é necessário** ter Python ou Airflow instalados localmente — tudo roda dentro dos containers.

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/finance-etl.git
cd finance-etl
```

**2. Configure as variáveis de ambiente**

```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais (veja a seção abaixo)
```

**3. Suba os containers**

```bash
docker compose up -d
```

**4. Acesse o Airflow**

Abra [http://localhost:8080](http://localhost:8080) no navegador.
- Usuário padrão: `airflow`
- Senha padrão: `airflow`

**5. Ative a DAG**

Na interface do Airflow, ative a DAG `finance_pipeline` e dispare a primeira execução manualmente ou aguarde o agendamento.

**6. Conecte o Power BI**

Abra o arquivo `financas.pbix` e aponte a conexão para `localhost:5432` com as credenciais do seu `.env`.

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# PostgreSQL
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=finance_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://seu_usuario:sua_senha@postgres/airflow
AIRFLOW__CORE__FERNET_KEY=sua_fernet_key
```

---

## 🚀 Pipeline em Ação

### Airflow — Tasks em execução

<img width="1050" height="359" alt="Captura de tela 2026-05-04 182428" src="https://github.com/user-attachments/assets/5c6e5516-c89c-490e-8a74-1a414554fccc" />



As 3 tasks rodam em sequência com dependência explícita:

```
extrair_dados >> transformar_dados >> carregar_no_postgres
```

### PostgreSQL — Dados armazenados

<img width="445" height="486" alt="Captura de tela 2026-05-04 182804" src="https://github.com/user-attachments/assets/2a27be28-d491-46a1-b26b-1bceb325d311" />


---

## 📊 Dashboard Interativo

Acesse o dashboard pelo link abaixo:

🔗 **[Abrir no Power BI](https://app.powerbi.com/view?r=eyJrIjoiZDE5YmRkNzktYmU0NS00ZGNjLWEwNDEtNTJiMThhZDQyNTYzIiwidCI6IjFkMDkwYmUwLTEyYjctNGJhNi05M2E0LTQzZmM0NWExNzk2NSJ9)**

---


## 👤 Autor

Feito por **Cleiton Silva** — conecte-se no [LinkedIn](https://www.linkedin.com/in/cleiton-silveira21/) ou veja mais projetos no [GitHub](https://github.com/Cleitondev01/).

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
