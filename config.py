import os
from dotenv import load_dotenv

load_dotenv()

dbHost = os.environ.get("dbHost")
dbuser = os.environ.get("dbuser")
dbpasswd = os.environ.get("dbpasswd")
dbport = os.environ.get("dbport")
db = os.environ.get("db")
