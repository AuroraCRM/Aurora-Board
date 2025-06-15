from fastapi import FastAPI, Depends, HTTPException
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
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db)):
    return services.create_board(db=db, board=board)

@app.get("/boards/{board_id}", response_model=schemas.Board)
def read_board(board_id: int, db: Session = Depends(get_db)):
    db_board = services.get_board(db, board_id=board_id)
    if db_board is None: # Should be handled by service, but good practice for belt-and-suspenders
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

@app.get("/boards/", response_model=PyList[schemas.Board])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boards = services.get_boards(db, skip=skip, limit=limit)
    return boards

@app.put("/boards/{board_id}", response_model=schemas.Board)
def update_board(board_id: int, board: schemas.BoardUpdate, db: Session = Depends(get_db)):
    return services.update_board(db=db, board_id=board_id, board_update=board)

@app.delete("/boards/{board_id}", status_code=200) # Or 204 if no content is returned
def delete_board(board_id: int, db: Session = Depends(get_db)):
    # The service layer returns a dict like {"detail": "Board deleted successfully"}
    # Or you can have the service return the deleted object (or None) and handle response here
    return services.delete_board(db=db, board_id=board_id)


# List Endpoints
@app.post("/lists/", response_model=schemas.ListSchema, status_code=201)
def create_list(list_create: schemas.ListSchemaCreate, db: Session = Depends(get_db)):
    # Ensure board exists (service does this, but can be double-checked)
    # services.get_board(db, board_id=list_create.board_id)
    return services.create_list(db=db, list_create_data=list_create)

@app.get("/lists/{list_id}", response_model=schemas.ListSchema)
def read_list(list_id: int, db: Session = Depends(get_db)):
    db_list = services.get_list(db, list_id=list_id)
    if db_list is None: # Service handles this
        raise HTTPException(status_code=404, detail="List not found")
    return db_list

@app.get("/boards/{board_id}/lists/", response_model=PyList[schemas.ListSchema])
def read_lists_for_board(board_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # services.get_board(db, board_id=board_id) # Ensure board exists (service does this)
    lists = services.get_lists_by_board(db, board_id=board_id, skip=skip, limit=limit)
    return lists

@app.put("/lists/{list_id}", response_model=schemas.ListSchema)
def update_list(list_id: int, list_update: schemas.ListSchemaUpdate, db: Session = Depends(get_db)):
    return services.update_list(db=db, list_id=list_id, list_update=list_update)

@app.delete("/lists/{list_id}", status_code=200)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    return services.delete_list(db=db, list_id=list_id)


# Card Endpoints
@app.post("/cards/", response_model=schemas.Card, status_code=201)
def create_card(card_create: schemas.CardCreate, db: Session = Depends(get_db)):
    # services.get_list(db, list_id=card_create.list_id) # Ensure list exists (service does this)
    return services.create_card(db=db, card_create_data=card_create)

@app.get("/cards/{card_id}", response_model=schemas.Card)
def read_card(card_id: int, db: Session = Depends(get_db)):
    db_card = services.get_card(db, card_id=card_id)
    if db_card is None: # Service handles this
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@app.get("/lists/{list_id}/cards/", response_model=PyList[schemas.Card])
def read_cards_for_list(list_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # services.get_list(db, list_id=list_id) # Ensure list exists (service does this)
    cards = services.get_cards_by_list(db, list_id=list_id, skip=skip, limit=limit)
    return cards

@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, card_update: schemas.CardUpdate, db: Session = Depends(get_db)):
    return services.update_card(db=db, card_id=card_id, card_update=card_update)

@app.delete("/cards/{card_id}", status_code=200)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    return services.delete_card(db=db, card_id=card_id)

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
