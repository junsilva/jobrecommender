import logging
import logging.config
import structlog
import time

from functools import wraps
from pathlib import Path

# from structlog.processors import CallsiteParameter
import orjson


LEVEL = "INFO"
LOG_FOLDER = "./logs"
LOG_FILENAME = "app.log"


def configure_logging():
    log_directory = Path(LOG_FOLDER)
    log_directory.mkdir(parents=True, exist_ok=True)

    # Define the logging configuration in a dictionary
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {"format": "%(message)s"},  # For structlog JSON rendering
        },
        "handlers": {
            "rotating_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_directory / LOG_FILENAME,
                "maxBytes": 5242880,  # 5 MB
                "backupCount": 3,
                "formatter": "json",
            },
        },
        "loggers": {
            "my_logger": {
                "level": LEVEL,
                "handlers": ["rotating_file_handler"],
                "propagate": False,
            }
        },
        "root": {"level": LEVEL, "handlers": ["rotating_file_handler"]},
    }

    # Apply the logging configuration
    logging.config.dictConfig(log_config)

    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.EventRenamer("msg"),
            structlog.contextvars.merge_contextvars,
            structlog.processors.JSONRenderer(serializer=orjson.dumps),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def unbind_func_contextvars(func):
    """Decorator to unbind context variables during function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Unbind all currently bound context variables
        bound_vars = structlog.contextvars.bound_contextvars
        existing_context = bound_vars.get()

        try:
            # Clear the context variables
            bound_vars.unbind()

            # Call the original function
            result = func(*args, **kwargs)

            return result
        finally:
            # Restore the original context
            if existing_context:
                bound_vars.bind(**existing_context)

    return wrapper


def time_execution(logger):
    """Decorator to measure execution time of a function and log it at the end."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            # Calculate execution time
            execution_time = end_time - start_time

            # Log the execution time as part of the last log call
            logger.info(f"Timing for function={func.__name__} done.  {execution_time=}")

            return result

        return wrapper

    return decorator
