from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List as PyList

from . import services, models, schemas
from .database import SessionLocal, engine

# Create database tables if they don't exist
# In a production app, you might use Alembic for migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aurora Board API",
    description="Backend for a Kanban-style board application, designed for future AI integration.",
    version="0.1.0"
)

# CORS Middleware Configuration
# Defina as origens permitidas. Para desenvolvimento, "*" pode ser usado,
# mas para produção, especifique os domínios do frontend.
origins = [
    "http://localhost:5173",  # Endereço padrão do Vite dev server
    "http://127.0.0.1:5173", # Alternativa para o Vite dev server
    # Adicione aqui o endereço do seu frontend em produção
    # "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite origens específicas
    allow_credentials=True, # Permite cookies e cabeçalhos de autenticação
    allow_methods=["*"],    # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Permite todos os cabeçalhos
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes

# Board Endpoints
@app.post("/boards/", response_model=schemas.Board, status_code=201)
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.create_board(db=db, board=board, current_user_id=current_user.id)

@app.get("/boards/{board_id}", response_model=schemas.Board)
def read_board(board_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    # Service layer now handles not found and permission checks
    return services.get_board(db, board_id=board_id, current_user_id=current_user.id)

@app.get("/boards/", response_model=PyList[schemas.Board])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.get_boards(db, current_user_id=current_user.id, skip=skip, limit=limit)

@app.put("/boards/{board_id}", response_model=schemas.Board)
def update_board(board_id: int, board: schemas.BoardUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.update_board(db=db, board_id=board_id, board_update=board, current_user_id=current_user.id)

@app.delete("/boards/{board_id}", status_code=200) # Or 204 if no content is returned
def delete_board(board_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.delete_board(db=db, board_id=board_id, current_user_id=current_user.id)


# List Endpoints
@app.post("/lists/", response_model=schemas.ListSchema, status_code=201)
def create_list(list_create: schemas.ListSchemaCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.create_list(db=db, list_create_data=list_create, current_user_id=current_user.id)

@app.get("/lists/{list_id}", response_model=schemas.ListSchema)
def read_list(list_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.get_list(db, list_id=list_id, current_user_id=current_user.id)

@app.get("/boards/{board_id}/lists/", response_model=PyList[schemas.ListSchema])
def read_lists_for_board(board_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.get_lists_by_board(db, board_id=board_id, current_user_id=current_user.id, skip=skip, limit=limit)

@app.put("/lists/{list_id}", response_model=schemas.ListSchema)
def update_list(list_id: int, list_update: schemas.ListSchemaUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.update_list(db=db, list_id=list_id, list_update=list_update, current_user_id=current_user.id)

@app.delete("/lists/{list_id}", status_code=200)
def delete_list(list_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.delete_list(db=db, list_id=list_id, current_user_id=current_user.id)


# Card Endpoints
@app.post("/cards/", response_model=schemas.Card, status_code=201)
def create_card(card_create: schemas.CardCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.create_card(db=db, card_create_data=card_create, current_user_id=current_user.id)

@app.get("/cards/{card_id}", response_model=schemas.Card)
def read_card(card_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.get_card(db, card_id=card_id, current_user_id=current_user.id)

@app.get("/lists/{list_id}/cards/", response_model=PyList[schemas.Card])
def read_cards_for_list(list_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.get_cards_by_list(db, list_id=list_id, current_user_id=current_user.id, skip=skip, limit=limit)

@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card_update: schemas.CardUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.update_card(db=db, card_id=card_id, card_update=card_update, current_user_id=current_user.id)

@app.delete("/cards/{card_id}", status_code=200)
def delete_card(card_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user_dependency)):
    return services.delete_card(db=db, card_id=card_id, current_user_id=current_user.id)

# Basic root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Aurora Board API"}

# To run this app (from the directory containing `aurora-board`):
# Create a .env file in aurora-board/backend/src/aurora_board/ with DATABASE_URL
# Example .env:
# DATABASE_URL="postgresql://user:password@host:port/database_name"
#
# Then run:
# uvicorn aurora_board.backend.src.aurora_board.main:app --reload --app-dir aurora-board/backend/src
# Or if you are in aurora-board/backend/src:
# uvicorn aurora_board.main:app --reload
#
# If `aurora_board.backend.src` is not in python path, you might need to adjust the python path or how uvicorn is called.
# A common practice is to run from the project root and specify the app module path.
# Example, if you are in the `aurora-board` directory:
# PYTHONPATH=./backend/src uvicorn aurora_board.main:app --reload

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from . import security as auth_security
from .security import get_current_user as get_current_user_dependency # Renamed for clarity
from .models import User as UserModel # To type hint the dependency
from datetime import timedelta

# Authentication Endpoint
@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = services.get_user_by_username(db, username=form_data.username)
    if not user or not auth_security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User Registration Endpoint
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return services.create_user(db=db, user=user)
