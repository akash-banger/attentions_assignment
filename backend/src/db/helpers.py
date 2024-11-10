from sqlalchemy.exc import SQLAlchemyError
from .database import get_session, User
from uuid import UUID

def create_user(username: str, password: str) -> User:
    session = get_session()
    try:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user) 
        return new_user
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_by_id(id: UUID) -> User:
    session = get_session()
    try:
        user = session.query(User).filter(User.id == id).first()
        return user
    except SQLAlchemyError as e:
        print(e)
    finally:
        session.close()
    
def get_user_by_username(username: str) -> User:
    session = get_session()
    try:
        user = session.query(User).filter(User.username == username).first()
        return user
    except SQLAlchemyError as e:
        raise e
    finally:
        session.close()





