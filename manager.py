import uvicorn
import logging
from app import create_app, Config

from app.models.database import engine, Base
from app.utils.logger import log_setup
import argparse

log_setup(filename=Config.log_base_dir + Config.log_file)
print(Config)
log = logging.getLogger(__name__)

app = create_app()


def run():
    uvicorn.run(app, port=10000, host="127.0.0.1", log_level='info')

def init_db(fresh=False):
    # if fresh:
    #     Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    log.info("Application is Starting Up")

@app.on_event("shutdown")
async def shutdown():
    log.info("Application is Shutting Down")

def parse_args():
    parser = argparse.ArgumentParser(description="Database Initialization Script")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database")
    parser.add_argument("--populate-db", action="store_true", help="opulate the database")
    return parser.parse_args()

def initialize_db():
    args = parse_args()
    print("ALL_ARGS: ",args)
    if args.init_db:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully.")
        exit(0)
    if  args.populate_db:
        print("pop initialized successfully.")
        # populate_user_data()
if __name__ == '__main__':
    initialize_db()
    run()
