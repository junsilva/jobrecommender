"""Entry point for the Recommender application.

Additional commands should be registered under the cli group.

For now, only csv_input command is implemented.
"""

import click
import structlog
from . import commands
from . import logging_config


logging_config.configure_logging()


@click.group()
def cli():
    """Serve as the main command for the application.

    Click expects this to be empty.
    """
    pass


cli.add_command(commands.csv_input)


if __name__ == "__main__":
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    logger.info("##### START UP #####")
    cli()
