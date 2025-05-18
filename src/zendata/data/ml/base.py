from typing import Optional
from pydantic import Field
from zendata.data.base import BaseData


class BaseMLData(BaseData):
    source_id: Optional[str] = Field(None, description="Source id of the data")
