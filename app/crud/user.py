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

    def __init__(self, db, current_user:User):
        self.db = db
        self.current_user = current_user
    
    def fetch_user(self):
        """
        Fetch user
        :return: True if success else False
        """
        try:
            users = self.db.query(User).all()
            if users:
                return True, users
            return False, f'No users found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the users - {e}')
            return False, f'Facing issue while fetching the users'
        
    def fetch_user_by_id(self, user_id: str):
        """
        Fetch user by id
        :param user_id: Id of the user
        :return: True if success else False
        """
        try:
            user_data = self.db.query(User).filter(User.id == user_id).first()
            if user_data:
                return True, user_data
            return False, f'User with id {user_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the user with id {user_id} - {e}')
            return False, f'Facing issue while fetching the user with id {user_id}'
        
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
            if not self.current_user.is_superuser():
                logger.error(f'User is not a superuser {self.current_user.id}')
                return False, f'User is not a superuser {self.current_user.id}'
            # UserSchema(**user)
            logger.info(f'INFO: Creating new user with the data - {user}')
            resp, msg = self.fetch_user_by_name(user.name)
            if resp:
                
                logger.error(f'User with name {user.name} is already registered')
                return False, f'User with name {user.name} is already registered'
            if not resp and msg is None:
                print("resp",msg)
                logger.error(msg)
                return False, msg
            logger.info(f'INFO: Created user ORM with - {user.name}')
            new_user = User(name=user.name,
                            email=user.email,
                            password= get_password_hash(user.password),
                            role=user.role,
                            is_active=0,
                            created_by=self.current_user.email,
                            creation_time=datetime.now(),
                            modification_time=datetime.now())
            logger.info(f'INFO: Saving the new user {user.name}')
            self.db.add(new_user)
            logger.info(f'INFO: Committing the new user {user.name}')
            self.db.commit()
            logger.info(f'INFO: New user {user.name} saved successfully')
            return True, f'New user {user.name} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new user {user.name} - {e}')
            return False, f'Facing issue while saving the new user {user.name}'

def get_password_hash(password: str):
    """
    Returns the password hash
    :param password: Password
    :return: Hashed password
    """
    return pwd_context.hash(password)