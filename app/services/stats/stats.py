import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.services.auth.auth_bearer import get_current_user
from app.models.user.user import User
from app.crud.transaction import TransactionDBActions

log = logging.getLogger(__name__)

class StatsService:
    method_decorators = [api_logger]

    def __init__(self):
        self.store_db_actions = None
    
    # fetch transaction stats by date filter #TODO 
    async def transaction_stats(self, request: Request, response: Response, db: Session = Depends(get_session),
                                 current_user: User= Depends(get_current_user),start_date: str = None, end_date: str = None):
        print('start_date',start_date)
        print('end_date',end_date)
        try:
            self.store_db_actions = TransactionDBActions(db,current_user)
            resp, msg = self.store_db_actions.get_transaction_stats()
            if resp:
                log.info(f'Transaction stats fetched successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the transaction stats - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while fetching the transaction stats - {e}')
            return Resp.error(response, f'Facing issue in transaction stats -{e}')