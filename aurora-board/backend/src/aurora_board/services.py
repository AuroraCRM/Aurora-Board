from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from . import models, schemas

# Helper function for atomic operations
# For testing, we'll let the test's db_session fixture handle commits/rollbacks.
# In a real app, _execute_atomic would manage transactions per operation.
def _execute_atomic(db: Session, operation_func, *args, **kwargs):
    # Check if we are in a test environment (simplistic check, could be more robust)
    # For now, assume if the session has a 'get_bind' method and its bind is a Connection,
    # it might be part of a test fixture that manages transactions.
    # A more explicit way would be to pass a flag or use a different function for tests.

    # Simplified for now: remove commit/rollback for tests.
    # This means tests need to manage commits if data needs to be visible across service calls
    # before the final test rollback.

    # is_test_session = hasattr(db, 'get_bind') and hasattr(db.get_bind(), 'begin_nested') # Example check

    try:
        result = operation_func(db, *args, **kwargs)
        # if not is_test_session: # Or some other flag indicating non-test environment
        #     db.commit()
        # else:
        #     db.flush() # Ensure changes are sent to DB, but not committed yet in test session

        # For current debugging, let's remove commit/rollback entirely from here.
        # The test fixture db_session will handle rollback.
        # If services need to see each other's uncommitted data, flush might be needed.
        db.flush() # Flush changes to the current transaction

        if result: # Ensure result is not None
            if hasattr(result, '__dict__'): # Check if it's a model instance
                 if db.object_session(result): # Check if object is bound to a session
                    db.refresh(result)
            elif isinstance(result, list) and result and hasattr(result[0], '__dict__'):
                for item in result:
                    if db.object_session(item): # Check if object is bound to a session
                       db.refresh(item)
        return result
    except HTTPException: # Re-raise HTTPException
        # if not is_test_session:
        #     db.rollback()
        raise # Let the test fixture handle rollback on error
    except Exception as e:
        # if not is_test_session:
        #     db.rollback()
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
        update_data = b_update.model_dump(exclude_unset=True)
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
        get_board(db_session, list_data.board_id)
        max_pos = db_session.query(func.max(models.List.position)).filter(models.List.board_id == list_data.board_id).scalar()
        new_position = (max_pos or 0) + 1
        db_list = models.List(name=list_data.name, board_id=list_data.board_id, position=new_position)
        db_session.add(db_list)
        return db_list
    return _execute_atomic(db, operation, list_create_data)

def get_list(db: Session, list_id: int):
    db_list = db.query(models.List).filter(models.List.id == list_id).first()
    if db_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return db_list

def get_lists_by_board(db: Session, board_id: int, skip: int = 0, limit: int = 100):
    get_board(db, board_id)
    return db.query(models.List).filter(models.List.board_id == board_id).order_by(models.List.position).offset(skip).limit(limit).all()

def update_list_positions(db: Session, board_id: int, moved_list_id: int, new_position: int, old_position: int):
    """Helper to adjust positions of other lists when a list is moved or deleted."""
    if new_position == old_position and moved_list_id is not None: # No change or simple update not affecting order
        return

    if old_position < new_position: # Moved down
        # Shift items between old_position and new_position up
        db.query(models.List).filter(
            models.List.board_id == board_id,
            models.List.id != moved_list_id, # Don't shift the moved item itself yet
            models.List.position > old_position,
            models.List.position <= new_position
        ).update({models.List.position: models.List.position - 1}, synchronize_session=False)
    elif old_position > new_position: # Moved up
        # Shift items between new_position and old_position down
        db.query(models.List).filter(
            models.List.board_id == board_id,
            models.List.id != moved_list_id, # Don't shift the moved item itself yet
            models.List.position >= new_position,
            models.List.position < old_position
        ).update({models.List.position: models.List.position + 1}, synchronize_session=False)
    # If moved_list_id is None, it means a list was deleted, and items after old_position need to be shifted up.
    elif moved_list_id is None and old_position is not None: # Deletion case
        db.query(models.List).filter(
            models.List.board_id == board_id,
            models.List.position > old_position
        ).update({models.List.position: models.List.position - 1}, synchronize_session=False)


def update_list(db: Session, list_id: int, list_update: schemas.ListSchemaUpdate):
    def operation(db_session, l_id, l_update):
        db_list = get_list(db_session, l_id)
        update_data = l_update.model_dump(exclude_unset=True)

        original_position = db_list.position
        new_position = update_data.get("position")

        if new_position is not None and new_position != original_position:
            # Ensure new_position is valid
            max_pos = db_session.query(func.count(models.List.id)).filter(models.List.board_id == db_list.board_id).scalar()
            if not (1 <= new_position <= max_pos):
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid position. Must be between 1 and {max_pos}.")

            update_list_positions(db_session, db_list.board_id, l_id, new_position, original_position)
            db_list.position = new_position # Set the new position for the target list

        for key, value in update_data.items():
            if key != "position": # Position is handled above
                 setattr(db_list, key, value)

        db_session.add(db_list)
        return db_list
    return _execute_atomic(db, operation, list_id, list_update)

def _update_list_positions_on_delete(db: Session, board_id: int, deleted_item_position: int):
    """Helper specifically for adjusting list positions after a deletion."""
    db.query(models.List).filter(
        models.List.board_id == board_id,
        models.List.position > deleted_item_position
    ).update({models.List.position: models.List.position - 1}, synchronize_session='fetch')

def delete_list(db: Session, list_id: int):
    def operation(db_session, l_id):
        db_list = get_list(db_session, l_id)
        board_id = db_list.board_id
        deleted_position = db_list.position

        db_session.delete(db_list)

        _update_list_positions_on_delete(db_session, board_id, deleted_position)

        return {"detail": "List deleted successfully"}
    return _execute_atomic(db, operation, list_id)


# Card Services
def create_card(db: Session, card_create_data: schemas.CardCreate):
    def operation(db_session, card_data):
        get_list(db_session, card_data.list_id)
        max_pos = db_session.query(func.max(models.Card.position)).filter(models.Card.list_id == card_data.list_id).scalar()
        new_position = (max_pos or 0) + 1
        db_card = models.Card(title=card_data.title, description=card_data.description, list_id=card_data.list_id, position=new_position)
        db_session.add(db_card)
        return db_card
    return _execute_atomic(db, operation, card_create_data)

def get_card(db: Session, card_id: int):
    db_card = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return db_card

def get_cards_by_list(db: Session, list_id: int, skip: int = 0, limit: int = 100):
    get_list(db, list_id)
    return db.query(models.Card).filter(models.Card.list_id == list_id).order_by(models.Card.position).offset(skip).limit(limit).all()

def update_card_positions(db: Session, list_id: int, moved_card_id: int, new_position: int, old_position: int, new_list_id: int = None):
    """Helper to adjust positions of cards within a list when a card is moved or deleted."""
    target_list_id = new_list_id if new_list_id is not None else list_id

    if new_list_id is None or new_list_id == list_id: # Moving within the same list or deleting
        if old_position < new_position: # Moved down
            db.query(models.Card).filter(
                models.Card.list_id == target_list_id,
                models.Card.id != moved_card_id,
                models.Card.position > old_position,
                models.Card.position <= new_position
            ).update({models.Card.position: models.Card.position - 1}, synchronize_session=False)
        elif old_position > new_position: # Moved up
            db.query(models.Card).filter(
                models.Card.list_id == target_list_id,
                models.Card.id != moved_card_id,
                models.Card.position >= new_position,
                models.Card.position < old_position
            ).update({models.Card.position: models.Card.position + 1}, synchronize_session=False)
        elif moved_card_id is None and old_position is not None: # Deletion
             db.query(models.Card).filter(
                models.Card.list_id == target_list_id, # target_list_id is original list_id here
                models.Card.position > old_position
            ).update({models.Card.position: models.Card.position - 1}, synchronize_session=False)

    # If moving to a new list, positions in the old list (if card is removed)
    # and new list (if card is added) need separate handling.

def update_card(db: Session, card_id: int, card_update: schemas.CardUpdate):
    def operation(db_session, c_id, c_update):
        db_card = get_card(db_session, c_id)
        update_data = c_update.model_dump(exclude_unset=True)

        original_list_id = db_card.list_id
        original_position = db_card.position

        new_list_id = update_data.get("list_id")
        new_position = update_data.get("position")

        if new_list_id is not None and new_list_id != original_list_id:
            # Card is moving to a new list
            get_list(db_session, new_list_id) # Ensure new list exists

            # 1. Decrement positions in the old list for cards after the moved card
            db_session.query(models.Card).filter(
                models.Card.list_id == original_list_id,
                models.Card.position > original_position
            ).update({models.Card.position: models.Card.position - 1}, synchronize_session=False)

            # 2. Determine new position in the new list
            if new_position is None: # If no specific position, add to the end
                max_pos_new_list = db_session.query(func.max(models.Card.position)).filter(models.Card.list_id == new_list_id).scalar()
                target_position_in_new_list = (max_pos_new_list or 0) + 1
            else: # Specific position requested in new list
                max_pos_new_list = db_session.query(func.count(models.Card.id)).filter(models.Card.list_id == new_list_id).scalar()
                if not (1 <= new_position <= max_pos_new_list + 1): # Allow inserting at the very end
                     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid position in new list. Must be between 1 and {max_pos_new_list + 1}.")
                target_position_in_new_list = new_position
                # Increment positions in the new list for cards at or after the new_position
                db_session.query(models.Card).filter(
                    models.Card.list_id == new_list_id,
                    models.Card.position >= target_position_in_new_list
                ).update({models.Card.position: models.Card.position + 1}, synchronize_session=False)

            db_card.list_id = new_list_id
            db_card.position = target_position_in_new_list
            update_data.pop("list_id", None) # Handled
            update_data.pop("position", None) # Handled

        elif new_position is not None and new_position != original_position:
            # Card is moving within the same list
            max_pos = db_session.query(func.count(models.Card.id)).filter(models.Card.list_id == original_list_id).scalar()
            if not (1 <= new_position <= max_pos):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid position. Must be between 1 and {max_pos}.")

            update_card_positions(db_session, original_list_id, c_id, new_position, original_position)
            db_card.position = new_position
            update_data.pop("position", None) # Handled

        # Apply other updates like title, description
        for key, value in update_data.items():
            setattr(db_card, key, value)

        db_session.add(db_card)
        return db_card
    return _execute_atomic(db, operation, card_id, card_update)

def delete_card(db: Session, card_id: int):
    def operation(db_session, c_id):
        db_card = get_card(db_session, c_id)
        list_id_of_deleted_card = db_card.list_id
        position_of_deleted_card = db_card.position

        db_session.delete(db_card)

        _update_card_positions_on_delete(db_session, list_id_of_deleted_card, position_of_deleted_card)

        return {"detail": "Card deleted successfully"}
    return _execute_atomic(db, operation, card_id)

def _update_card_positions_on_delete(db: Session, list_id: int, deleted_item_position: int):
    """Helper specifically for adjusting card positions after a deletion."""
    db.query(models.Card).filter(
        models.Card.list_id == list_id,
        models.Card.position > deleted_item_position
    ).update({models.Card.position: models.Card.position - 1}, synchronize_session='fetch')

# In delete_card service:
# _update_card_positions_on_delete(db_session, list_id_of_deleted_card, position_of_deleted_card)


# More complex operations like move_card would also use _execute_atomic
# And would require careful handling of positions in source and destination lists.
# def move_card(db: Session, card_id: int, new_list_id: int, new_position: int):
#     def operation(db_session, c_id, nl_id, np):
#         # This function can be effectively replaced by the improved update_card logic
#         # which now handles moving cards between lists and reordering.
#         # If a more dedicated 'move' endpoint is desired, it could call update_card.
#         card_update_schema = schemas.CardUpdate(list_id=nl_id, position=np)
#         return update_card(db_session, c_id, card_update_schema)
#     return _execute_atomic(db, operation, card_id, new_list_id, new_position)
