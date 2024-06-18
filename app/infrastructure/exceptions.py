from functools import wraps
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

class RepositoryError(Exception):
    """Base class for all repository errors."""
    pass

class RepositoryConnectionError(RepositoryError):
    """Raised when there is a connection error with the database."""
    pass

class RepositoryNotFoundError(RepositoryError):
    """Raised when a requested item is not found in the database."""
    pass

class RepositoryOperationError(RepositoryError):
    """Raised when there is a general error performing a database operation."""
    pass

def handle_repository_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ServerSelectionTimeoutError as timeout_exception:
            args[0].logger.error(f'Time out al conectar con la base de datos: {timeout_exception}')
            raise RepositoryConnectionError(f'Time out al conectar con la base de datos: {timeout_exception}')
        except PyMongoError as pymongo_exception:
            args[0].logger.error(f"Error en la base de datos: {pymongo_exception}")
            raise RepositoryOperationError(f"Error en la base de datos: {pymongo_exception}")
        except Exception as exception:
            args[0].logger.error(f"Error inesperado: {exception}")
            raise RepositoryOperationError(f"Error inesperado: {exception}")
    return wrapper
