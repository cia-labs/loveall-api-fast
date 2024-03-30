import logging

from typing import Any, Union

from pydantic import BaseModel
from starlette.responses import Response
from app.config import Config
from app.models.user import User
from app.schema.user import UserResponse, UserSchema

log = logging.getLogger(__name__)

class RespModel(BaseModel):
    status: str
    # version_info: dict
    class Config:
        orm_mode = True


class RespUserModel(BaseModel):
    # __response__: Response 
    status: int
    data: Union[UserResponse,str]


class Resp:

    @staticmethod
    def success(response: Response, resp_data: str = None, meta_data: str = None, status=200, **kwargs):
        """
        success
        ---
        returns response format for successful response and status as 200.
        Arguments:
            response: Response
            resp_data: dict
            meta_data: dict
            status: int
        """
        if resp_data is None:
            resp_data = {}
        output_data = {'status': 'success', 'version_info': dict(version=Config.VERSION_INFO),
                       'data': resp_data}
        if meta_data:
            output_data['meta'] = meta_data
        if kwargs.get('supported_version'):
            output_data['supported_version'] = kwargs.get('supported_version')
        if kwargs.get('logs'):
            output_data['logs'] = kwargs.get('logs')
        response.status_code = status
        return output_data

    @staticmethod
    def error(response: Response, message: str = None, status=400, **kwargs):
        """
        error
        ---
        returns response format for error response and status as 400.
        Arguments:
            response: Response
            message: string
            status: int
        """
        output_data = {'status': 'error', 'version_info': dict(version=Config.VERSION_INFO),
                       'message': message}
        if kwargs.get('supported_version'):
            output_data['supported_version'] = kwargs.get('supported_version')
        if kwargs.get('logs'):
            output_data['logs'] = kwargs.get('logs')
        response.status_code = status
        return output_data
