# Sistema de Controle de Ponto – Python + Oracle

**Disciplina:** Banco de Dados  
**Professor:** Howard Roatti  
**Instituição:** FAESA  
**Última atualização:** Outubro/2025  
**Vídeo de Apresentação: https://youtu.be/FCXpp0ONjVg**
Integrantes: Hellen Karla Costa, Júlia Ogassavara e Yasmim Luiz
Turma: 4SC1
---

## Descrição do Projeto

O **Sistema de Controle de Ponto** tem como objetivo registrar as marcações de entrada e saída dos funcionários, calcular jornadas de trabalho, controlar faltas e gerar relatórios de presença e horas trabalhadas.

Este projeto foi desenvolvido em **Python**, com integração direta ao **banco de dados Oracle**, simulando um sistema real de interface entre uma linguagem de programação e um banco relacional.

O sistema implementa operações **CRUD completas (Create, Read, Update, Delete)** sobre as entidades **Funcionário** e **Marcação**, além de dois relatórios obrigatórios:
1. **Relatório com funções agregadas (GROUP BY);**  
2. **Relatório com junção de tabelas (JOIN).**

---

## Requisitos do Ambiente

### Software Necessário
- **Python 3.10+** instalado no sistema;
- **Banco de Dados Oracle** acessível e configurado;
- **Oracle Instant Client** instalado (instruções abaixo);
- Dependências listadas no arquivo:
  ```
  src/requirements.txt
  ```

Instale as dependências com:
```bash
pip install -r src/requirements.txt
```

---

## Estrutura do Projeto

```
.
├── diagrams/                      # Diagramas ER e de sequência
├── sql/                           # Scripts SQL de criação e consultas
├── src/
│   ├── conexion/
│   │   └── oracle_queries.py      # Conexão e execução de comandos SQL
│   ├── controller/
│   │   ├── controller_funcionario.py
│   │   └── controller_marcacao.py # Controladores CRUD
│   ├── model/
│   │   ├── funcionario.py
│   │   └── marcacao.py            # Classes de domínio
│   ├── reports/
│   │   └── relatorios.py          # Relatórios de frequência e horas
│   ├── utils/
│   │   ├── config.py              # Menus e configurações
│   │   └── splash_screen.py       # Tela inicial com contagem de registros
│   ├── create_tables_and_records.py
│   ├── principal.py               # Ponto de entrada da aplicação (CLI)
│   ├── test.py                    # Testes e exemplos de uso
│   └── requirements.txt           # Dependências Python
└── README.md
```

---

## Execução do Projeto no Linux

1. **Clonar o repositório do GitHub:**
   ```bash
   git clone https://github.com/<seu_usuario>/<nome_do_repositorio>.git
   cd <nome_do_repositorio>
   ```

2. **Criar e ativar ambiente virtual (recomendado):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Criar tabelas e inserir registros de exemplo:**
   ```bash
   python src/create_tables_and_records.py
   ```

5. **Executar o sistema principal (menu interativo):**
   ```bash
   python src/principal.py
   ```

6. **Encerrar o ambiente virtual:**
   ```bash
   deactivate
   ```

---

## Exemplos de Uso (Módulo `OracleQueries`)

### Consulta:
```python
from conexion.oracle_queries import OracleQueries

query = "SELECT cpf, nome FROM funcionarios ORDER BY nome"
oracle = OracleQueries()
oracle.connect()
df = oracle.sqlToDataFrame(query)
print(df)
```

### Inserção:
```python
oracle = OracleQueries(can_write=True)
oracle.connect()
oracle.write("INSERT INTO funcionarios (cpf, nome) VALUES ('00000000000', 'Fulano')")
```

---

## Relatórios Implementados

1. **Relatório de Horas Trabalhadas (Agrupamento / GROUP BY):**
   - Soma de horas trabalhadas por funcionário em determinado período.

2. **Relatório de Marcações (Junção / JOIN):**
   - Exibe nome do funcionário, data e horários de entrada e saída.

---

## Instalação do Oracle Instant Client (Linux)

1. Baixe a versão compatível em:  
   🔗 [https://www.oracle.com/database/technologies/instant-client.html](https://www.oracle.com/database/technologies/instant-client.html)

2. Se o arquivo for `.rpm`, converta e instale:
   ```bash
   sudo apt install alien
   sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
   ```

3. Configure as variáveis de ambiente:
   ```bash
   sudo mkdir -p /usr/local/oracle/instantclient_18_5/
   sudo mv lib /usr/local/oracle/instantclient_18_5/
   echo 'export ORACLE_HOME=/usr/local/oracle/instantclient_18_5' >> ~/.bash_profile
   echo 'export LD_LIBRARY_PATH=$ORACLE_HOME/lib' >> ~/.bash_profile
   echo 'export PATH=$PATH:$ORACLE_HOME/bin' >> ~/.bash_profile
   source ~/.bash_profile
   ```

---

## Solução de Problemas Comuns

**Erro:** `ORA-28001: the password has expired`  
> Execute os comandos abaixo no Oracle (como DBA):
```sql
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
ALTER USER labdatabase IDENTIFIED BY "labDatabase2022";
```
---




