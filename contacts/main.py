from fastapi import FastAPI

from .routers import contacts


app = FastAPI()

app.include_router(contacts.router)


@app.get('/')
async def root():
    return {
        'message': 'Hello FastAPI!'
    }
