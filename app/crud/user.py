import json
import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from app.models import user
from app.models.user import ActiveToken, User
from app.schema.user import UserRegister, UserSchema
import logging

from app.utils.utils import pwd_context

logger = logging.getLogger(__name__)


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
        
    def fetch_user_by_email(self, email: str)->tuple:
        """
        Fetch user by email
        :param email: Email of the user
        :return: True if success else False
        """
        try:
            print("DEBUG")
            print("DEBUG 2: ",self.db.query(User).all())
            user_data = self.db.query(User).filter(User.email == email).first()
            # print(user_data)
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

    def register_new_user(self, user: UserRegister):
        """
        Register new user
        :param user: New user details
        :return: True if success else False
        """
        try:
            new_user = User(name=user.name,
                            email=user.email,
                            password= get_password_hash(user.password),
                            role="customer",
                            is_active=0,
                            created_by="",
                            creation_time=datetime.now(),
                            modification_time=datetime.now())
            self.db.add(new_user)
            self.db.commit()
            return True, f'New user {user.name} saved successfully'
        except IntegrityError as ie:
            logger.exception(f'User with email {user.email} is already registered')
            return False, f'User with email {user.email} is already registered'
        except Exception as e:

            logger.exception(f'Facing issue while saving the new user {user.name} - {e}')
            return False, f'Facing issue while saving the new user {user.name}'

    def generate_activation_token(self, user: User):
        """
        Generate activation token
        :param user: User details
        :return: True if success else False
        """
        try:
            token = str(uuid.uuid4())
            new_token = ActiveToken(user_id=user.id,
                                    token=token,
                                    expiry=datetime.now(),
                                    used=0,
                                    creation_time=datetime.now(),
                                    modification_time=datetime.now())
            
            self.db.add(new_token)
            self.db.commit()
            return True, token
        except Exception as e:
            logger.exception(f'Facing issue while generating activation token for user {user.name} - {e}')
            return False, f'Facing issue while generating activation token for user {user.name}'
        
    def verify_activation_token(self, user_id:int,token: str):
        """
        Verify activation token
        :param user_id: User id
        :param token: Token
        :return: True if success else False
        """
        try:
            print(user_id,token)
            token_data = self.db.query(ActiveToken).filter(ActiveToken.user_id == user_id, ActiveToken.token == token).first()
            print(token_data)
            if not token_data:
                return False, f'Invalid token'
            if token_data.used == 1:
                return False, f'Token already used'
            self.db.query(User).filter(User.id == user_id).update({'is_active': 1})
            self.db.query(ActiveToken).filter(ActiveToken.user_id == user_id, ActiveToken.token == token).update({'used': 1})
            self.db.commit()
            return True, f'Activation successful'
        except Exception as e:
            logger.exception(f'Facing issue while verifying the activation token for user {user_id} - {e}')
            return False, f'Facing issue while verifying the activation token for user {user_id}'


    def save_new_user(self, user: UserSchema):
        """
        Save new user
        :param user: New user details
        :return: True if success else False
        """
        try:
            print(self.current_user)
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