import os
from dotenv import load_dotenv

load_dotenv()

dbHost = os.environ.get("host")
dbuser = os.environ.get("user")
dbpasswd = os.environ.get("password")
dbport = os.environ.get("port")
db = os.environ.get("database")