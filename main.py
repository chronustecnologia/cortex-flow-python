from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.init_db import init_db
from api.v1 import auth
from core.dependencies import get_current_user

app = FastAPI(title="Cortex Flow API")

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    init_db(db)

app.include_router(auth.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root(current_user: dict = Depends(get_current_user)):
    return {"message": "Welcome to Cortex Flow API!"}

from api.v1 import database
from api.v1 import table
from api.v1 import column
from api.v1 import foreign_key
from api.v1 import index
from api.v1 import relationship
from api.v1 import ai_model
from api.v1 import parameter
from api.v1 import conversation
from api.v1 import message
from api.v1 import chat

app.include_router(database.router, prefix="/api/v1", tags=["Database"])
app.include_router(table.router, prefix="/api/v1", tags=["Table"])
app.include_router(column.router, prefix="/api/v1", tags=["Column"])
app.include_router(foreign_key.router, prefix="/api/v1", tags=["Foreign Key"])
app.include_router(index.router, prefix="/api/v1", tags=["Index"])
app.include_router(relationship.router, prefix="/api/v1", tags=["Relationship"])
app.include_router(ai_model.router, prefix="/api/v1", tags=["AI Model"])
app.include_router(parameter.router, prefix="/api/v1", tags=["Parameter"])
app.include_router(conversation.router, prefix="/api/v1", tags=["Conversation"])
app.include_router(message.router, prefix="/api/v1", tags=["Message"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
