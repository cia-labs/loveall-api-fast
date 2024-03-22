import os
from passlib.context import CryptContext
pwd_context =CryptContext(schemes=["sha256_crypt"], deprecated="auto")

from minio import Minio

minio_client = Minio(os.getenv("MINIO_HOSTNAME"),
                     access_key=os.getenv("MINIO_ACCESS_KEY"),
                     secret_key=os.getenv("MINIO_SECRET_KEY"),
                     secure=False)  # Change to True if using HTTPS

MINIO_BUCKET_NAME=os.getenv("MINIO_BUCKET_NAME")