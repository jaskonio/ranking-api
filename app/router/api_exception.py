"""_summary_
"""


class ApiException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """
    def __init__(self, code_error:int, name: str):
        self.code_error = code_error
        self.message = name
