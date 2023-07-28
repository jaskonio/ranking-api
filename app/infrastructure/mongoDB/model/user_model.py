"""_summary_
"""
from pydantic import BaseModel

class UserModel(BaseModel):
    """_summary_
    """
    user_name: str
    password: str
