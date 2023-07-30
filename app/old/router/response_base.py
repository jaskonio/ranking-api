"""_summary_
"""
from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")

class IResponseBase(GenericModel):
    """_summary_

    Args:
        GenericModel (_type_): _description_
        Generic (_type_): _description_
    """
    items: Optional[DataType] = None
    meta: dict = {}
    message: str = ""
