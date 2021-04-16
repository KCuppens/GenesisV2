import logging
from logging.config import dictConfig


# Taken from https://github.com/nvie/rq/blob/master/rq/logutils.py
def setup_loghandlers(level=None):
    # Setup logging for email_backend if not already configured
    logger = logging.getLogger('email_backend')
    if not logger.handlers:
        dictConfig({
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "email_backend": {
                    "format": "[%(levelname)s]%(asctime)s PID %(process)d: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },

            "handlers": {
                "email_backend": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "email_backend"
                },
            },

            "loggers": {
                "email_backend": {
                    "handlers": ["email_backend"],
                    "level": level or "DEBUG"
                }
            }
        })
    return logger