__all__ = ["DBUser"]

import bcrypt
from sqlalchemy import String, Column

from .base import DBModel


class DBUser(DBModel):
    __tablename__ = 'users'

    username = Column(String(256), nullable=False, unique=True)
    password_encrypted = Column(String(1024), nullable=True)

    @property
    def password(self):
        return self.password_encrypted

    @password.setter
    def password(self, password: str):
        password_encoded = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_encoded, salt)
        self.password_encrypted = password_hash.decode('utf-8')

    def compare_password(self, password: str):
        if self.password is None or password is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_encrypted.encode('utf-8'))
