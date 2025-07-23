from pydantic import BaseModel, Field

class News(BaseModel):
    title: str
    text: str
    url: str