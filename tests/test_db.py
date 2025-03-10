from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import Todo, TodoState, User


def test_create_user(session: Session, mock_db_time):
    user_info = {
        'username': 'kruger',
        'password': 'pwd123',
        'email': 'ricardo@kruger.com',
    }

    with mock_db_time(model=User) as time:
        new_user = User(**user_info)
        session.add(new_user)
        session.commit()

    user = session.scalar(
        select(User).where(User.username == user_info['username'])
    )

    assert asdict(user) == {
        'id': 1,
        **user_info,
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state=TodoState.draft,
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
