from fastapi import APIRouter
from app.services.transaction.transaction import TransactionService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer,get_current_user


class TransactionRouter:
    """
    Router for transaction    
    """

    def __init__(self):
        """
        Constructor for subscriptiontype router
        """
        self.transactionRouter = TransactionService()
        self.router = APIRouter(prefix='/transaction',tags=['transaction'])
        self.router.add_api_route(path='/{transaction_id:path}', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.transactionRouter.fetch_transaction)
        
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.transactionRouter.create_transaction)
        self.router.add_api_route(path='/update/{transaction_id:path}', methods=['PATCH'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.transactionRouter.update_transaction)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.storeService.delete_s)