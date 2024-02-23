import json
import uuid
from datetime import datetime

from app.models.transaction.transaction import Transaction
from app.schema.transaction import TransactionSchema
from app.utils.logger import api_logger
import logging

from passlib.context import CryptContext
logger = logging.getLogger(__name__)

class TransactionDBActions:
    method_decorators = [api_logger]
    def __init__(self, db,current_user):
        self.db = db
        self.current_user = current_user

    def fetch_transaction_by_id(self, transaction_id: str):
        """
        Fetch transaction by id
        :param transaction_id: Id of the transaction
        :return: True if success else False
        """
        try:
            transaction= None
            if self.current_user.is_superuser():
                transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).all()
            else:
                transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).filter(Transaction.merchant_user_id==self.current_user.id).all()
            if transaction:
                return True, transaction
            return False, f'Transaction with id {transaction_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the transaction with id {transaction_id} - {e}')
            return False, f'Facing issue while fetching the transaction with id {transaction_id}'
        
    def fetch_transaction(self):
        """
        Fetch transaction
        :return: True if success else False
        """
        try:
            transaction = None
            if self.current_user.is_superuser():
                transaction = self.db.query(Transaction).all()
            elif self.current_user.role == 'merchant':
                transaction = self.db.query(Transaction).filter(Transaction.merchant_user_id == self.current_user.id).all()
            else:
                transaction = self.db.query(Transaction).filter(Transaction.user_id == self.current_user.id).all()
            if transaction:
                return True, transaction
            return True,[]
        except Exception as e:
            logger.exception(f'Facing issue while fetching the transaction - {e}')
            return False, f'Facing issue while fetching the transaction'
        
    def save_new_transaction(self, transaction: TransactionSchema):
        """
        Save new transaction
        """
        try:
            self.db.add(Transaction(**transaction.dict(),**{
               "merchant_user_id": self.current_user.id,
               "created_by": self.current_user.email,
               "creation_time": datetime.now(),
                "modification_time": datetime.now(),
            }))
            self.db.commit()
            return True, f'Transaction {transaction} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new transaction - {e}')
            return False, f'Facing issue while saving the new transaction - {e}'
        
    def update_transaction(self, transaction : TransactionSchema,transaction_id: str):
        """
        Update transaction
        """
        try:
            result = None
            final_update = {**transaction.dict(),"modification_time": datetime.now()}
            if not self.current_user.is_superuser():
                result = self.db.query(Transaction).filter(Transaction.id == transaction_id).update(final_update)
            else:
                result = self.db.query(Transaction).filter(Transaction.id == transaction_id).filter(Transaction.merchant_user_id==self.current_user.id).update(final_update)
            if result==0:
                return False, f'Transaction with id {transaction_id} not found'
            self.db.commit()
            return True, f'Transaction {transaction} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the transaction - {e}')
            return False, f'Facing issue while updating the transaction - {e}'