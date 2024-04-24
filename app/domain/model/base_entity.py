from app.core.mapper_utils import class_to_dict


class BaseEntity():
    def __init__(self) -> None:
        pass

    def to_dict(self):
        return class_to_dict(self)
