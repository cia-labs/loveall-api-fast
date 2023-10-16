import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.transaction import TransactionDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.transaction import TransactionSchema
from app.models.user.user import User
from app.models.transaction.transaction import Transaction
from app.services.auth.auth_bearer import get_current_user

log = logging.getLogger(__name__)

class TransactionService:
    method_decorators = [api_logger]

    def __init__(self):
        self.store_db_actions = None
    
    async def fetch_transaction(self,transaction_id:str,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        """
        Fetch transaction
        :return: True if success else False
        """
        try:
            self.store_db_actions = TransactionDBActions(db,current_user)
            result,msg = None,None
            if transaction_id and len(transaction_id)>0:
                result, msg =  self.store_db_actions.fetch_transaction_by_id(transaction_id)
            else:
                result, msg = self.store_db_actions.fetch_transaction()
            if result:
                return Resp.success(response,msg)
            return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while fetching the transaction - {e}')
            return Resp.error(response, f'Facing issue in transaction -{e}')
    
    async def fetch_transactions(self,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        """
        Fetch transaction
        :return: True if success else False
        """
        try:
            self.store_db_actions = TransactionDBActions(db,current_user)
            status, transaction = self.store_db_actions.fetch_transaction()
            if status:
                return Resp(data=transaction).success()
            return Resp().not_found(message=transaction)
        except Exception as e:
            log.exception(f'Facing issue while fetching the transaction - {e}')
            return Resp().internal_server_error(message=f'Facing issue while fetching the transaction - {e}')
    
    async def create_transaction(self,transaction: TransactionSchema,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        """
        Save new transaction
        """
        try:
            self.store_db_actions = TransactionDBActions(db,current_user)
            status, message = self.store_db_actions.save_new_transaction(transaction)
            if status:
                return Resp.success(response,message)
            return Resp().bad_request(message=message)
        except Exception as e:
            log.exception(f'Facing issue while saving the new transaction - {e}')
            return Resp().internal_server_error(message=f'Facing issue while saving the new transaction - {e}')
        
    async def update_transaction(self,transaction_id:str,transaction: TransactionSchema,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        """
        Update transaction
        """
        try:
            self.store_db_actions = TransactionDBActions(db,current_user)
            status, message = self.store_db_actions.update_transaction(transaction,transaction_id)
            if status:
                return Resp(data=message).success()
            return Resp().bad_request(message=message)
        except Exception as e:
            log.exception(f'Facing issue while updating the transaction - {e}')
            return Resp().internal_server_error(message=f'Facing issue while updating the transaction - {e}')
        