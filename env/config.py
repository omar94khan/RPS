from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), 'dev.env')
load_dotenv(dotenv_path)

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')

ROUTER_PATH = os.getenv('ROUTER_PATH')

