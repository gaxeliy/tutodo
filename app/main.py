import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app import users, tasks
from app.config import DEBUG, WORKERS_COUNT
from app.helpers import get_response_class

app = FastAPI()


app.include_router(tasks.router.router)
app.include_router(users.router.router)


@app.get('/', response_class=HTMLResponse)
async def index():
    with open('templates/index.html', 'r') as f:
        return f.read()


if __name__ == '__main__':
    if DEBUG:
        uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
    else:
        uvicorn.run('main:app', host='0.0.0.0', port=8000, workers=WORKERS_COUNT)
