from math import e
import os
from typing import Any
from passlib.context import CryptContext
pwd_context =CryptContext(schemes=["sha256_crypt"], deprecated="auto")

from minio import Minio

minio_client = Minio(os.getenv("MINIO_HOSTNAME"),
                     access_key=os.getenv("MINIO_ACCESS_KEY"),
                     secret_key=os.getenv("MINIO_SECRET_KEY"),
                     secure=False)  # Change to True if using HTTPS

MINIO_BUCKET_NAME=os.getenv("MINIO_BUCKET_NAME")



def convert_to(from_obj:dict,to_obj:Any):
    data = {}
    for field in list(to_obj.__fields__.keys()):
        if from_obj.get(field):
            if field == "role":
                data[field] =  from_obj.get(field).value
            else:
                data[field] =  from_obj.get(field)
    
    return to_obj(**data)


# function to do post  call with basic auth to uri https://lall-n8n.cialabs.tech/webhook/fc9b37c2-bfd3-48b1-8a48-5b0c5bc09170 
def post_to_n8n(data:dict):
    import requests
    try:
        uri = os.getenv("N8N_ACTIVATE_HOOK_URL")
        response = requests.post(uri,json=data,auth=(os.get("N8N_ACTIVATE_HOOK_USER"),os.getenv("N8N_ACTIVATE_HOOK_PASS")))
        return True,response.json()
    except Exception as e:
        print(f"Error in post_to_n8n: {e}")
        return False,str(e)
