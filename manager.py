import logging
from logging.config import dictConfig
import uvicorn
from app import create_app, Config
from app.models.database import engine, Base
import argparse
# from app.services.auth import auth
from app.utils.logger import LogConfig

dictConfig(LogConfig().dict())


log = logging.getLogger(__name__)

app = create_app()
# auth.handle_errors(app)


def run():
    uvicorn.run(app, port=10000, host="127.0.0.1", log_level='debug',log_config=LogConfig().dict())

def init_db(fresh=False):
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    log.debug("Application is Starting Up")

@app.on_event("shutdown")
async def shutdown():
    log.debug("Application is Shutting Down")

def parse_args():
    parser = argparse.ArgumentParser(description="Database Initialization Script")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database")
    parser.add_argument("--populate-db", action="store_true", help="opulate the database")
    return parser.parse_args()

def initialize_db():
    args = parse_args()
    log.debug(f"args: {args}")
    if args.init_db:
        Base.metadata.create_all(bind=engine)
        log.debug("Database initialized successfully.")
        exit(0)
    if  args.populate_db:
        log.debug("pop initialized successfully.")

if __name__ == '__main__':
    log.debug("Starting the application")
    initialize_db()
    run()
