import uvicorn
from fastapi import FastAPI

from .routers import contacts, auth


app = FastAPI()

app.include_router(contacts.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {
        'message': 'Hello FastAPI!'
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
