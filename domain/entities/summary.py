from pydantic import BaseModel, Field
from typing import List

class Summary(BaseModel):
    title: str
    description: str
    url: str

class SummaryList(BaseModel):
    summaries: List[Summary]