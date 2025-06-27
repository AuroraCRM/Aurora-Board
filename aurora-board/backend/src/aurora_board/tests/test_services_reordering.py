import pytest
from sqlalchemy.orm import Session as SQLAlchemySession
from fastapi import HTTPException

from aurora_board import services, schemas, models

# Helper function to create multiple lists for a board
def create_lists(db_session: SQLAlchemySession, board: models.Board, count: int) -> list[models.List]:
    lists = []
    for i in range(1, count + 1):
        list_schema = schemas.ListSchemaCreate(name=f"List {i}", board_id=board.id)
        # Directly use the operation part of the service for test setup, or use the service
        # If using service, ensure commit happens if service doesn't commit itself in a way tests can see
        # Here, create_list service handles commit via _execute_atomic
        created_list = services.create_list(db=db_session, list_create_data=list_schema)
        lists.append(created_list)
    db_session.commit() # Commit after creating all lists in the batch
    for lst in lists: # Refresh to get any server-side changes (like IDs if not already populated by flush)
        if db_session.object_session(lst): # Ensure it's still part of a session that can refresh
             db_session.refresh(lst)
    return lists

# Helper function to create multiple cards for a list
def create_cards(db_session: SQLAlchemySession, list_obj: models.List, count: int) -> list[models.Card]:
    cards = []
    for i in range(1, count + 1):
        card_schema = schemas.CardCreate(title=f"Card {i}", list_id=list_obj.id)
        created_card = services.create_card(db=db_session, card_create_data=card_schema)
        cards.append(created_card)
    db_session.commit() # Commit after creating all cards in the batch
    for card in cards: # Refresh
        if db_session.object_session(card):
            db_session.refresh(card)
    return cards

def get_list_positions(db_session: SQLAlchemySession, board_id: int) -> list[tuple[int, int]]:
    return [(lst.id, lst.position) for lst in db_session.query(models.List).filter(models.List.board_id == board_id).order_by(models.List.position).all()]

def get_card_positions(db_session: SQLAlchemySession, list_id: int) -> list[tuple[int, int]]:
    return [(card.id, card.position) for card in db_session.query(models.Card).filter(models.Card.list_id == list_id).order_by(models.Card.position).all()]


# --- List Reordering Tests ---

def test_create_list_positioning(db_session: SQLAlchemySession, test_board: models.Board):
    """Test that lists are created with sequential positions."""
    list1 = services.create_list(db_session, schemas.ListSchemaCreate(name="L1", board_id=test_board.id))
    assert list1.position == 1
    list2 = services.create_list(db_session, schemas.ListSchemaCreate(name="L2", board_id=test_board.id))
    assert list2.position == 2
    list3 = services.create_list(db_session, schemas.ListSchemaCreate(name="L3", board_id=test_board.id))
    assert list3.position == 3

    positions = get_list_positions(db_session, test_board.id)
    assert positions == [(list1.id, 1), (list2.id, 2), (list3.id, 3)]

def test_delete_list_reorders_subsequent(db_session: SQLAlchemySession, test_board: models.Board):
    """Test that deleting a list reorders subsequent lists."""
    lists = create_lists(db_session, test_board, 4) # L1, L2, L3, L4 at pos 1,2,3,4

    services.delete_list(db_session, lists[1].id) # Delete L2 (original pos 2)

    db_session.expire_all() # Expire to ensure fresh data from DB

    remaining_lists = db_session.query(models.List).filter(models.List.board_id == test_board.id).order_by(models.List.position).all()
    assert len(remaining_lists) == 3
    assert remaining_lists[0].id == lists[0].id and remaining_lists[0].position == 1 # L1
    assert remaining_lists[1].id == lists[2].id and remaining_lists[1].position == 2 # L3 is now pos 2
    assert remaining_lists[2].id == lists[3].id and remaining_lists[2].position == 3 # L4 is now pos 3

def test_delete_last_list(db_session: SQLAlchemySession, test_board: models.Board):
    lists = create_lists(db_session, test_board, 3) # L1, L2, L3
    services.delete_list(db_session, lists[2].id) # Delete L3
    db_session.expire_all()
    remaining_positions = get_list_positions(db_session, test_board.id)
    assert len(remaining_positions) == 2
    assert remaining_positions == [(lists[0].id, 1), (lists[1].id, 2)]

def test_update_list_position_move_down(db_session: SQLAlchemySession, test_board: models.Board):
    """Move L1 (pos 1) to pos 3. Expected: L2 -> pos 1, L3 -> pos 2, L1 -> pos 3"""
    lists = create_lists(db_session, test_board, 4) # L1, L2, L3, L4
    l1, l2, l3, l4 = lists[0], lists[1], lists[2], lists[3]

    services.update_list(db_session, l1.id, schemas.ListSchemaUpdate(position=3))
    db_session.expire_all()

    new_positions = get_list_positions(db_session, test_board.id)
    assert new_positions == [(l2.id, 1), (l3.id, 2), (l1.id, 3), (l4.id, 4)]

def test_update_list_position_move_up(db_session: SQLAlchemySession, test_board: models.Board):
    """Move L3 (pos 3) to pos 1. Expected: L3 -> pos 1, L1 -> pos 2, L2 -> pos 3"""
    lists = create_lists(db_session, test_board, 4)
    l1, l2, l3, l4 = lists[0], lists[1], lists[2], lists[3]

    services.update_list(db_session, l3.id, schemas.ListSchemaUpdate(position=1))
    db_session.expire_all()

    new_positions = get_list_positions(db_session, test_board.id)
    assert new_positions == [(l3.id, 1), (l1.id, 2), (l2.id, 3), (l4.id, 4)]


def test_update_list_position_invalid_low(db_session: SQLAlchemySession, test_board: models.Board):
    lists = create_lists(db_session, test_board, 3)
    with pytest.raises(HTTPException) as exc_info:
        services.update_list(db_session, lists[0].id, schemas.ListSchemaUpdate(position=0))
    assert exc_info.value.status_code == 400

def test_update_list_position_invalid_high(db_session: SQLAlchemySession, test_board: models.Board):
    lists = create_lists(db_session, test_board, 3) # Max pos is 3
    with pytest.raises(HTTPException) as exc_info:
        services.update_list(db_session, lists[0].id, schemas.ListSchemaUpdate(position=4))
    assert exc_info.value.status_code == 400

def test_update_list_position_no_change(db_session: SQLAlchemySession, test_board: models.Board):
    lists = create_lists(db_session, test_board, 3)
    l1, l2, l3 = lists[0], lists[1], lists[2]
    services.update_list(db_session, l2.id, schemas.ListSchemaUpdate(position=2, name="Updated L2"))
    db_session.expire_all()

    updated_l2 = services.get_list(db_session, l2.id)
    assert updated_l2.name == "Updated L2"
    assert updated_l2.position == 2

    new_positions = get_list_positions(db_session, test_board.id)
    assert new_positions == [(l1.id, 1), (l2.id, 2), (l3.id, 3)]


# --- Card Reordering Tests ---

def test_create_card_positioning(db_session: SQLAlchemySession, test_list: models.List):
    """Test that cards are created with sequential positions within a list."""
    card1 = services.create_card(db_session, schemas.CardCreate(title="C1", list_id=test_list.id))
    assert card1.position == 1
    card2 = services.create_card(db_session, schemas.CardCreate(title="C2", list_id=test_list.id))
    assert card2.position == 2

    positions = get_card_positions(db_session, test_list.id)
    assert positions == [(card1.id, 1), (card2.id, 2)]

def test_delete_card_reorders_subsequent(db_session: SQLAlchemySession, test_list: models.List):
    """Test deleting a card reorders subsequent cards in the same list."""
    cards = create_cards(db_session, test_list, 4) # C1, C2, C3, C4 at pos 1,2,3,4

    services.delete_card(db_session, cards[1].id) # Delete C2 (original pos 2)
    db_session.expire_all()

    remaining_cards = db_session.query(models.Card).filter(models.Card.list_id == test_list.id).order_by(models.Card.position).all()
    assert len(remaining_cards) == 3
    assert remaining_cards[0].id == cards[0].id and remaining_cards[0].position == 1 # C1
    assert remaining_cards[1].id == cards[2].id and remaining_cards[1].position == 2 # C3 is now pos 2
    assert remaining_cards[2].id == cards[3].id and remaining_cards[2].position == 3 # C4 is now pos 3

def test_update_card_position_move_down_same_list(db_session: SQLAlchemySession, test_list: models.List):
    """Move C1 (pos 1) to pos 3 in the same list."""
    cards = create_cards(db_session, test_list, 4) # C1, C2, C3, C4
    c1, c2, c3, c4 = cards[0], cards[1], cards[2], cards[3]

    services.update_card(db_session, c1.id, schemas.CardUpdate(position=3))
    db_session.expire_all()

    new_positions = get_card_positions(db_session, test_list.id)
    assert new_positions == [(c2.id, 1), (c3.id, 2), (c1.id, 3), (c4.id, 4)]

def test_update_card_position_move_up_same_list(db_session: SQLAlchemySession, test_list: models.List):
    """Move C3 (pos 3) to pos 1 in the same list."""
    cards = create_cards(db_session, test_list, 4)
    c1, c2, c3, c4 = cards[0], cards[1], cards[2], cards[3]

    services.update_card(db_session, c3.id, schemas.CardUpdate(position=1))
    db_session.expire_all()

    new_positions = get_card_positions(db_session, test_list.id)
    assert new_positions == [(c3.id, 1), (c1.id, 2), (c2.id, 3), (c4.id, 4)]

def test_update_card_position_invalid_low_same_list(db_session: SQLAlchemySession, test_list: models.List):
    cards = create_cards(db_session, test_list, 3)
    with pytest.raises(HTTPException) as exc_info:
        services.update_card(db_session, cards[0].id, schemas.CardUpdate(position=0))
    assert exc_info.value.status_code == 400

def test_update_card_position_invalid_high_same_list(db_session: SQLAlchemySession, test_list: models.List):
    cards = create_cards(db_session, test_list, 3) # Max pos is 3
    with pytest.raises(HTTPException) as exc_info:
        services.update_card(db_session, cards[0].id, schemas.CardUpdate(position=4))
    assert exc_info.value.status_code == 400

# --- Card Moving Between Lists Tests ---

def test_move_card_to_another_list_end(db_session: SQLAlchemySession, test_board: models.Board):
    list1 = services.create_list(db_session, schemas.ListSchemaCreate(name="L1", board_id=test_board.id))
    list2 = services.create_list(db_session, schemas.ListSchemaCreate(name="L2", board_id=test_board.id))

    cards_l1 = create_cards(db_session, list1, 3) # C1, C2, C3 in L1
    cards_l2 = create_cards(db_session, list2, 2) # C4, C5 in L2 (relative to list2)

    card_to_move = cards_l1[0] # C1 from L1 (pos 1)

    # Move C1 from L1 to L2 (should be at the end of L2, pos 3)
    services.update_card(db_session, card_to_move.id, schemas.CardUpdate(list_id=list2.id))
    db_session.expire_all()

    # Check L1
    l1_cards_pos = get_card_positions(db_session, list1.id)
    assert len(l1_cards_pos) == 2
    assert l1_cards_pos[0] == (cards_l1[1].id, 1) # C2 is now pos 1
    assert l1_cards_pos[1] == (cards_l1[2].id, 2) # C3 is now pos 2

    # Check L2
    l2_cards_pos = get_card_positions(db_session, list2.id)
    assert len(l2_cards_pos) == 3
    assert l2_cards_pos[0] == (cards_l2[0].id, 1) # C4 (original in L2)
    assert l2_cards_pos[1] == (cards_l2[1].id, 2) # C5 (original in L2)
    assert l2_cards_pos[2] == (card_to_move.id, 3) # C1 is now at pos 3 in L2

def test_move_card_to_another_list_specific_position(db_session: SQLAlchemySession, test_board: models.Board):
    list1 = services.create_list(db_session, schemas.ListSchemaCreate(name="L1 B", board_id=test_board.id))
    list2 = services.create_list(db_session, schemas.ListSchemaCreate(name="L2 B", board_id=test_board.id))

    cards_l1 = create_cards(db_session, list1, 2) # C1, C2 in L1
    cards_l2 = create_cards(db_session, list2, 2) # C3, C4 in L2

    c1_l1, c2_l1 = cards_l1[0], cards_l1[1]
    c1_l2, c2_l2 = cards_l2[0], cards_l2[1] # Originally C3, C4

    # Move C1 (from L1, pos 1) to L2, position 1
    # Expected L2: C1 (new), C3 (orig), C4 (orig)
    services.update_card(db_session, c1_l1.id, schemas.CardUpdate(list_id=list2.id, position=1))
    db_session.expire_all()

    # Check L1
    l1_cards_pos = get_card_positions(db_session, list1.id)
    assert l1_cards_pos == [(c2_l1.id, 1)] # C2 is now pos 1 in L1

    # Check L2
    l2_cards_pos = get_card_positions(db_session, list2.id)
    # Expected: C1_L1 becomes pos 1. C1_L2 (orig C3) becomes pos 2. C2_L2 (orig C4) becomes pos 3.
    assert l2_cards_pos == [(c1_l1.id, 1), (c1_l2.id, 2), (c2_l2.id, 3)]


def test_move_card_to_another_list_invalid_position_high(db_session: SQLAlchemySession, test_board: models.Board):
    list1 = services.create_list(db_session, schemas.ListSchemaCreate(name="L1 C", board_id=test_board.id))
    list2 = services.create_list(db_session, schemas.ListSchemaCreate(name="L2 C", board_id=test_board.id))
    cards_l1 = create_cards(db_session, list1, 1) # C1 in L1
    create_cards(db_session, list2, 1) # C2 in L2 (list2 has 1 card, max_pos is 1, can insert at pos 2)

    with pytest.raises(HTTPException) as exc_info:
        # Try to move C1 to L2 at position 3 (invalid, should be 1 or 2)
        services.update_card(db_session, cards_l1[0].id, schemas.CardUpdate(list_id=list2.id, position=3))
    assert exc_info.value.status_code == 400

def test_move_card_to_empty_list(db_session: SQLAlchemySession, test_board: models.Board):
    list_with_card = services.create_list(db_session, schemas.ListSchemaCreate(name="L-NonEmpty", board_id=test_board.id))
    empty_list = services.create_list(db_session, schemas.ListSchemaCreate(name="L-Empty", board_id=test_board.id))

    card_to_move = create_cards(db_session, list_with_card, 1)[0]

    # Move card to empty_list, position 1 (only valid position)
    services.update_card(db_session, card_to_move.id, schemas.CardUpdate(list_id=empty_list.id, position=1))
    db_session.expire_all()

    assert len(get_card_positions(db_session, list_with_card.id)) == 0
    new_empty_list_cards = get_card_positions(db_session, empty_list.id)
    assert new_empty_list_cards == [(card_to_move.id, 1)]

    # Try to move to empty list at position 2 (invalid)
    card_to_move_again = create_cards(db_session, list_with_card, 1)[0] # Create another card
    with pytest.raises(HTTPException) as exc_info:
        services.update_card(db_session, card_to_move_again.id, schemas.CardUpdate(list_id=empty_list.id, position=3)) # empty_list now has 1 card, so pos 3 is invalid. Max new pos is 2.
    assert exc_info.value.status_code == 400


def test_update_card_title_without_position_change(db_session: SQLAlchemySession, test_list: models.List):
    cards = create_cards(db_session, test_list, 2)
    c1, c2 = cards[0], cards[1]

    services.update_card(db_session, c1.id, schemas.CardUpdate(title="Updated C1 Title"))
    db_session.expire_all()

    updated_c1 = services.get_card(db_session, c1.id)
    assert updated_c1.title == "Updated C1 Title"
    assert updated_c1.position == 1 # Position should not change

    current_positions = get_card_positions(db_session, test_list.id)
    assert current_positions == [(c1.id, 1), (c2.id, 2)]
