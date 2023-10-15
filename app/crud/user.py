import json
import uuid
from datetime import datetime

from app.models.user.user import User
from app.schema.user import UserSchema
import logging

from passlib.context import CryptContext

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDBActions:
    db = None

    def __init__(self, db):
        self.db = db
    
    def fetch_user_by_email(self, email: str):
        """
        Fetch user by email
        :param email: Email of the user
        :return: True if success else False
        """
        try:
            print(email)
            user_data = self.db.query(User).filter(User.email == email).first()
            print(user_data)
            if user_data:
                return True, user_data
            return False, f'User with email {email} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the user with email {email} - {e}')
            return False, f'Facing issue while fetching the user with email {email}'

    def fetch_user_by_name(self, name: str):
        """
        Fetch user by name
        :param name: Name of the user
        :return: True if success else False
        """
        try:
            users = self.db.query(User).filter(User.name == name).all()
            if users:
                return True, users
            return False, f'User with name {name} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the user with name {name} - {e}')
            return False, f'Facing issue while fetching the user with name {name}'

    def save_new_user(self, user: UserSchema):
        """
        Save new user
        :param user: New user details
        :return: True if success else False
        """
        try:
            # UserSchema(**user)
            logger.info(f'INFO: Creating new user with the data - {user}')
            resp, msg = self.fetch_user_by_name(user.get('name'))
            if resp:
                
                logger.error(f'User with name {user.get("name")} is already registered')
                return False, f'User with name {user.get("name")} is already registered'
            if not resp and msg is None:
                print("resp",msg)
                logger.error(msg)
                return False, msg
            logger.info(f'INFO: Created user ORM with - {user.get("name")}')
            new_user = User(name=user.get('name'),
                            email=user.get('email'),
                            password= get_password_hash(user.get('password')),
                            role=user.get('role'),
                            is_active=user.get('is_active'),
                            created_by=user.get('created_by'),
                            creation_time=datetime.now(),
                            modification_time=datetime.now())
            logger.info(f'INFO: Saving the new user {user.get("name")}')
            self.db.add(new_user)
            logger.info(f'INFO: Committing the new user {user.get("name")}')
            self.db.commit()
            logger.info(f'INFO: New user {user.get("name")} saved successfully')
            return True, f'New user {user.get("name")} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new user {user.get("name")} - {e}')
            return False, f'Facing issue while saving the new user {user.get("name")}'

def get_password_hash(password: str):
    """
    Returns the password hash
    :param password: Password
    :return: Hashed password
    """
    return pwd_context.hash(password)