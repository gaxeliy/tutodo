import os

from starlette.templating import Jinja2Templates

DEBUG = os.getenv('DEBUG', 'False') == 'True'

WORKERS_COUNT = int(os.getenv('WORKERS_COUNT', '4'))

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres')

templates = Jinja2Templates(directory='templates')
