from pydantic import BaseModel, ConfigDict
from typing import List as PyList, Optional
from datetime import datetime

# Card Schemas
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    # position will be handled by the service layer

class CardCreate(CardBase):
    list_id: int

class CardUpdate(CardBase):
    title: Optional[str] = None
    description: Optional[str] = None
    list_id: Optional[int] = None
    position: Optional[int] = None # Allow updating position directly if needed, e.g., drag-and-drop

class Card(CardBase):
    id: int
    list_id: int
    position: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# List Schemas (using ListSchema naming convention)
class ListSchemaBase(BaseModel):
    name: str
    # position will be handled by the service layer

class ListSchemaCreate(ListSchemaBase):
    board_id: int

class ListSchemaUpdate(ListSchemaBase):
    name: Optional[str] = None
    position: Optional[int] = None # Allow updating position directly

class ListSchema(ListSchemaBase):
    id: int
    board_id: int
    position: int
    cards: PyList[Card] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Board Schemas
class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    name: Optional[str] = None
    description: Optional[str] = None

class Board(BoardBase):
    id: int
    lists: PyList[ListSchema] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
