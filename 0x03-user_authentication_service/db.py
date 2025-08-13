#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)  # type: ignore
        Base.metadata.create_all(self._engine)  # type: ignore
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a user object"""
        user = User(email=email,  # type: ignore
                    hashed_password=hashed_password)  # type: ignore
        session = self._session
        session.add(user)
        session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table as filtered by
           the methods input arguments
        """
        result = self._session.query(
            User).filter_by(**kwargs).first()  # type: ignore
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user's attribute as passed and commit to db"""
        for key, value in kwargs.items():
            self._session.query(
                User).filter(
                    User.id == user_id).update({key: value})  # type: ignore
        self._session.commit()
