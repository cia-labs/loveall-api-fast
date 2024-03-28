from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    version: int = 1

    disable_existing_loggers: bool = False

    formatters: dict = {
        "extended": {
            '()': 'coloredlogs.ColoredFormatter',
            "format": "%(asctime)s - %(name)20s - %(levelname)6s - %(message)s",
            "datefmt": "[%d/%b/%Y %H:%M:%S]"
        },
        "ecs": {
          "()": "ecs_logging.StdlibFormatter"
        },
    }

    handlers: dict = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "extended",
            "stream": "ext://sys.stdout",
        },
        "debug_file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "extended",
            "filename": "/Users/surya.m/Documents/CIAECO/test/loveall-api-fast/debug.log",
            "encoding": "utf8",
            "delay": True,
        },
        "error_file_handler": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "extended",
            "filename": "/Users/surya.m/Documents/CIAECO/test/loveall-api-fast/error.log",
            "encoding": "utf8",
            "delay": True,
        }
    }

    loggers: dict = {
        # Fine-grained logging configuration for individual modules or classes
        # Use this to set different log levels without changing 'real' code.
        "myclasses": {
            "level": "DEBUG",
            "propagate": True
        },
        "usermessages": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["console"]
        }
    }
    root: dict = {
        "level": "DEBUG",
        "handlers": ["debug_file_handler", "error_file_handler", 'console'],
    }
    