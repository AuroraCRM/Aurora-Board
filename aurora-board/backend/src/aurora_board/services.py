from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from . import models, schemas

# Helper function for atomic operations
def _execute_atomic(db: Session, operation_func, *args, **kwargs):
    try:
        result = operation_func(db, *args, **kwargs)
        db.commit()
        if hasattr(result, '__dict__'): # Check if it's a model instance
             db.refresh(result)
        elif isinstance(result, list) and result and hasattr(result[0], '__dict__'): # Check for list of models
            for item in result:
                db.refresh(item)
        return result
    except HTTPException: # Re-raise HTTPException
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        # Log the exception e here if logging is set up
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An internal server error occurred.")

# Board Services
def create_board(db: Session, board: schemas.BoardCreate):
    def operation(db_session, board_data):
        db_board = models.Board(name=board_data.name, description=board_data.description)
        db_session.add(db_board)
        return db_board
    return _execute_atomic(db, operation, board)

def get_board(db: Session, board_id: int):
    db_board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if db_board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return db_board

def get_boards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Board).offset(skip).limit(limit).all()

def update_board(db: Session, board_id: int, board_update: schemas.BoardUpdate):
    def operation(db_session, b_id, b_update):
        db_board = get_board(db_session, b_id) # Reuse get_board for not-found check
        update_data = b_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_board, key, value)
        db_session.add(db_board)
        return db_board
    return _execute_atomic(db, operation, board_id, board_update)

def delete_board(db: Session, board_id: int):
    def operation(db_session, b_id):
        db_board = get_board(db_session, b_id) # Reuse get_board for not-found check
        db_session.delete(db_board)
        return {"detail": "Board deleted successfully"} # Or return the deleted board
    return _execute_atomic(db, operation, board_id)

# List Services
def create_list(db: Session, list_create_data: schemas.ListSchemaCreate):
    def operation(db_session, list_data):
        # Ensure board exists
        get_board(db_session, list_data.board_id) # Raises HTTPException if not found

        # Optimized position calculation
        current_list_count = db_session.query(func.count(models.List.id)).filter(models.List.board_id == list_data.board_id).scalar()
        new_position = current_list_count + 1

        db_list = models.List(
            name=list_data.name,
            board_id=list_data.board_id,
            position=new_position
        )
        db_session.add(db_list)
        return db_list
    return _execute_atomic(db, operation, list_create_data)

def get_list(db: Session, list_id: int):
    db_list = db.query(models.List).filter(models.List.id == list_id).first()
    if db_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return db_list

def get_lists_by_board(db: Session, board_id: int, skip: int = 0, limit: int = 100):
    # Ensure board exists
    get_board(db, board_id)
    return db.query(models.List).filter(models.List.board_id == board_id).order_by(models.List.position).offset(skip).limit(limit).all()

def update_list(db: Session, list_id: int, list_update: schemas.ListSchemaUpdate):
    def operation(db_session, l_id, l_update):
        db_list = get_list(db_session, l_id) # Not-found check
        update_data = l_update.dict(exclude_unset=True)

        if "position" in update_data:
            # Add logic to re-order other lists if necessary
            pass # For now, just updating the position directly

        for key, value in update_data.items():
            setattr(db_list, key, value)
        db_session.add(db_list)
        return db_list
    return _execute_atomic(db, operation, list_id, list_update)

def delete_list(db: Session, list_id: int):
    def operation(db_session, l_id):
        db_list = get_list(db_session, l_id) # Not-found check
        # Add logic to update positions of subsequent lists if necessary
        db_session.delete(db_list)
        # Re-order remaining lists
        # lists_to_reorder = db_session.query(models.List).filter(
        #     models.List.board_id == db_list.board_id,
        #     models.List.position > db_list.position
        # ).order_by(models.List.position).all()
        # for i, list_item in enumerate(lists_to_reorder):
        #     list_item.position = db_list.position + i # This logic needs refinement for general re-ordering
        #     db_session.add(list_item)
        return {"detail": "List deleted successfully"}
    return _execute_atomic(db, operation, list_id)


# Card Services
def create_card(db: Session, card_create_data: schemas.CardCreate):
    def operation(db_session, card_data):
        # Ensure list exists
        get_list(db_session, card_data.list_id) # Raises HTTPException if not found

        # Optimized position calculation
        current_card_count = db_session.query(func.count(models.Card.id)).filter(models.Card.list_id == card_data.list_id).scalar()
        new_position = current_card_count + 1

        db_card = models.Card(
            title=card_data.title,
            description=card_data.description,
            list_id=card_data.list_id,
            position=new_position
        )
        db_session.add(db_card)
        return db_card
    return _execute_atomic(db, operation, card_create_data)

def get_card(db: Session, card_id: int):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return db_card

def get_cards_by_list(db: Session, list_id: int, skip: int = 0, limit: int = 100):
    # Ensure list exists
    get_list(db, list_id)
    return db.query(models.Card).filter(models.Card.list_id == list_id).order_by(models.Card.position).offset(skip).limit(limit).all()

def update_card(db: Session, card_id: int, card_update: schemas.CardUpdate):
    def operation(db_session, c_id, c_update):
        db_card = get_card(db_session, c_id) # Not-found check
        update_data = c_update.dict(exclude_unset=True)

        new_list_id_from_payload = update_data.get("list_id")
        original_list_id = db_card.list_id

        # Conditional logic: Compare local variables
        # DO NOT USE: if models.Card.list_id == new_list_id_from_payload:
        if new_list_id_from_payload is not None and new_list_id_from_payload != original_list_id:
            # Card is moving to a new list
            # Ensure new list exists
            get_list(db_session, new_list_id_from_payload)

            # Update positions in old list (simplified: just remove, re-ordering is complex)
            # cards_in_old_list = db_session.query(models.Card).filter(models.Card.list_id == original_list_id, models.Card.position > db_card.position).order_by(models.Card.position).all()
            # for i, card_item in enumerate(cards_in_old_list):
            #    card_item.position = db_card.position + i
            #    db_session.add(card_item)

            # Set new position in the new list
            if "position" not in update_data: # If position is not explicitly given for the new list
                current_card_count_new_list = db_session.query(func.count(models.Card.id)).filter(models.Card.list_id == new_list_id_from_payload).scalar()
                update_data["position"] = current_card_count_new_list + 1

        # Add more complex position handling if "position" is in update_data and list_id is also changing or not.
        # This part requires careful thought for re-ordering items in both old and new lists.
        # For now, if position is provided, it's taken directly. If list changes, new position is at the end.

        for key, value in update_data.items():
            setattr(db_card, key, value)

        db_session.add(db_card)
        return db_card
    return _execute_atomic(db, operation, card_id, card_update)

def delete_card(db: Session, card_id: int):
    def operation(db_session, c_id):
        db_card = get_card(db_session, c_id) # Not-found check
        # list_id_of_deleted_card = db_card.list_id
        # position_of_deleted_card = db_card.position
        db_session.delete(db_card)

        # Re-order remaining cards in the list (simplified)
        # cards_to_reorder = db_session.query(models.Card).filter(
        #     models.Card.list_id == list_id_of_deleted_card,
        #     models.Card.position > position_of_deleted_card
        # ).order_by(models.Card.position).all()
        # for i, card_item in enumerate(cards_to_reorder):
        #     card_item.position = position_of_deleted_card + i
        #     db_session.add(card_item)
        return {"detail": "Card deleted successfully"}
    return _execute_atomic(db, operation, card_id)

# More complex operations like move_card would also use _execute_atomic
# And would require careful handling of positions in source and destination lists.
# def move_card(db: Session, card_id: int, new_list_id: int, new_position: int):
#     def operation(db_session, c_id, nl_id, np):
#         db_card = get_card(db_session, c_id)
#         original_list_id = db_card.list_id
#         original_position = db_card.position

#         if original_list_id == nl_id: # Using local variable comparison
#             # Moving within the same list
#             # ... re-ordering logic ...
#             pass
#         else:
#             # Moving to a different list
#             get_list(db_session, nl_id) # Check if new list exists
#             # ... re-ordering logic for old list ...
#             # ... re-ordering logic for new list ...
#             db_card.list_id = nl_id

#         db_card.position = np
#         db_session.add(db_card)
#         return db_card
#     return _execute_atomic(db, operation, card_id, new_list_id, new_position)
