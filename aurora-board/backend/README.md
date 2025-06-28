# Aurora Board Backend

Este é o backend para a aplicação Aurora Board, construído com FastAPI.

## Configuração do Ambiente

1.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\\Scripts\\activate
    ```

2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` no diretório `src/aurora_board/` (ou seja, `aurora-board/backend/src/aurora_board/.env`).
    Este arquivo deve conter a URL de conexão do seu banco de dados:
    ```env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    ```
    Ou, para usar SQLite (ótimo para desenvolvimento rápido):
    ```env
    DATABASE_URL="sqlite:///./test.db"
    ```
    Se estiver usando SQLite, o arquivo `test.db` será criado no diretório `src/aurora_board/`.

## Migrações do Banco de Dados (Alembic)

Se houver alterações nos modelos SQLAlchemy (`src/aurora_board/models.py`), você precisará gerar e aplicar migrações.

1.  **Inicializar Alembic (apenas uma vez, se ainda não foi feito):**
    Certifique-se de que o `DATABASE_URL` está configurado em `src/aurora_board/alembic.ini` (ou que `env.py` o carrega corretamente).
    ```bash
    cd src/aurora_board
    alembic init alembic
    ```
    Depois, configure `env.py` em `src/aurora_board/alembic/env.py` para carregar seus modelos e a URL do banco de dados.

2.  **Gerar uma Nova Migração:**
    ```bash
    cd src/aurora_board
    # (Ajuste a mensagem conforme necessário)
    alembic revision -m "create_initial_tables"
    ```
    Edite o arquivo de script de migração gerado em `src/aurora_board/alembic/versions/` para definir as operações `upgrade` e `downgrade`.

3.  **Aplicar Migrações:**
    ```bash
    cd src/aurora_board
    alembic upgrade head
    ```

## Executando o Servidor de Desenvolvimento

A partir do diretório raiz do backend (`aurora-board/backend/`):
```bash
# Certifique-se que seu PYTHONPATH inclui o diretório src do backend
export PYTHONPATH=$PYTHONPATH:$(pwd)/src  # ou set PYTHONPATH=%PYTHONPATH%;%cd%\\src no Windows
# Ou execute diretamente com uvicorn especificando o app-dir
uvicorn aurora_board.main:app --reload --app-dir src
```
Alternativamente, de dentro do diretório `src/aurora_board`:
```bash
# Não recomendado se você tiver imports relativos à raiz do projeto src
# uvicorn main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`. A documentação da API (Swagger UI) estará em `http://127.0.0.1:8000/docs`.

## Executando Testes

A partir do diretório raiz do backend (`aurora-board/backend/`):
```bash
# Certifique-se de que pytest.ini está configurado ou PYTHONPATH está definido
pytest
```
É recomendado criar um arquivo `pytest.ini` na raiz de `aurora-board/backend/` com o seguinte conteúdo para garantir que os testes encontrem os módulos corretamente:
```ini
[pytest]
python_files = test_*.py tests_*.py *_test.py *_tests.py
pythonpath = src
```

## Estrutura do Projeto Backend

-   `src/aurora_board/`: Contém o código principal da aplicação.
    -   `main.py`: Ponto de entrada da aplicação FastAPI, define as rotas.
    -   `models.py`: Modelos SQLAlchemy (estrutura do banco de dados).
    -   `schemas.py`: Schemas Pydantic (validação de dados da API).
    -   `services.py`: Lógica de negócios.
    -   `database.py`: Configuração da conexão com o banco de dados.
    -   `security.py`: Utilitários de segurança (hash de senha, JWT).
    -   `.env`: (Não versionado) Variáveis de ambiente, como `DATABASE_URL`.
    -   `alembic/`: Diretório de configuração e versões do Alembic.
    -   `tests/`: Testes automatizados.
        -   `conftest.py`: Fixtures e configuração para Pytest.
-   `requirements.txt`: Dependências Python do projeto.
-   `README.md`: Este arquivo.
-   `pytest.ini`: (Recomendado) Configuração para Pytest.
```
