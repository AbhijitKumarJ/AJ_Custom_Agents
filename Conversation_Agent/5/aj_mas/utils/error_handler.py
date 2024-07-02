import traceback
from .logger import logger


class AJMASError(Exception):
    """Base class for AJ_MAS exceptions."""

    pass


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AJMASError as e:
            logger.error(f"AJ_MAS Error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise AJMASError(f"An unexpected error occurred: {str(e)}")

    return wrapper


def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None
