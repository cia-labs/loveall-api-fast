import json
import uuid
from datetime import datetime

from app.models.transaction import Transaction
from app.models.offer import Offer
from app.models.subscription import Subscription
from app.models.user import UserRole
from app.models.store import Store
from app.schema.transaction import TransactionSchema
import logging
import logging

from passlib.context import CryptContext
logger = logging.getLogger(__name__)

class TransactionDBActions:
    
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
                transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).filter(Transaction.merchant_id==self.current_user.id).all() # type: ignore
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
            data = []
            transaction=None
            # print(self.current_user.role,UserRole.MERCHANT)
            if self.current_user.is_superuser():
                transaction = self.db.query(Transaction).all()
                for transac in transaction:
                    data.append(transac)
                return True,data
            elif self.current_user.role == UserRole.MERCHANT:
                print("running Merfch")
                transaction = self.db.query(Transaction,Offer,Store,Subscription).join(Offer,Offer.id==Transaction.offer_id).join(Store,Store.id==Transaction.store_id).join(Subscription,Subscription.id==Transaction.subscription_id).all() # type: ignore
            else:
                print("running cus")
                transaction = self.db.query(Transaction,Offer,Store,Subscription).join(Offer,Offer.id==Transaction.offer_id).join(Store,Store.id==Transaction.store_id).join(Subscription,Subscription.id==Transaction.subscription_id).all() # type: ignore
            print(transaction)
            if transaction:
                for tnx,off,stor,sub in transaction:
                    cur_tnx = tnx.dict()
                    cur_tnx["offer"] = off
                    cur_tnx["store"] = stor
                    cur_tnx["subscription"] = sub
                    data.append(cur_tnx)
                return True, data
            return True,data
        except Exception as e:
            logger.exception(f'Facing issue while fetching the transaction - {e}')
            return False, f'Facing issue while fetching the transaction'
        
    def save_new_transaction(self, transaction: TransactionSchema):
        """
        Save new transaction
        """
        try:
            offer = self.db.query(Offer).filter(Offer.id == transaction.offer_id).first()
            if not offer:
                return False, f'Offer with id {transaction.offer_id} not found'
            subscription = self.db.query(Subscription).filter(Subscription.id == transaction.subscription_id).first()
            if not subscription:
                return False, f'Subscription with id {transaction.subscription_id} not found'
            
            offer_amount = transaction.total_amount - (transaction.total_amount * offer.discount_rate/100)

            self.db.add(Transaction(**transaction.dict(),**{
               "merchant_id": self.current_user.id,
               "created_by": self.current_user.email,
               "creation_time": datetime.now(),
                "modification_time": datetime.now(),
                "discount_rate": offer.discount_rate,
                "customer_id": subscription.customer_id,
                "store_id": offer.store_id,
                "offer_amount" : offer_amount
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
                result = self.db.query(Transaction).filter(Transaction.id == transaction_id).filter(Transaction.merchant_id==self.current_user.id).update(final_update) # type: ignore
            if result==0:
                return False, f'Transaction with id {transaction_id} not found'
            self.db.commit()
            return True, f'Transaction {transaction} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the transaction - {e}')
            return False, f'Facing issue while updating the transaction - {e}'
        
                
    def get_transaction_stats(self):
        """
        Get transaction stats
        if merchant get no of transaction and total amount 
        if customer get no of transaction and total amount saved
        """
        try:
            result = None
            if not self.current_user.is_superuser():
                result = self.db.query(Transaction).filter(Transaction.user_id == self.current_user.id).all() # type: ignore
            else:
                result = self.db.query(Transaction).filter(Transaction.merchant_id == self.current_user.id).all() # type: ignore
            if result:
                return True, result
            return True, []
        except Exception as e:
            logger.exception(f'Facing issue while getting the transaction stats - {e}')
            return False, f'Facing issue while getting the transaction stats - {e}'