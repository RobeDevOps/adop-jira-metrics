import os
import sys
import logging
import watcher.logger
import serializer.logger
from controller.agile_portafolio import AgilePortafolio


def main():
    LOGS_PATH = os.environ.get('LOGS_PATH')
    DATA_PATH = os.environ.get('DATA_PATH')

    watcher.logger.init(LOGS_PATH)
    logger = logging.getLogger('JIRA-LOGS')
    logger.info("Starting collection of agile-portafolio metrics")

    try:

        agile_portafolio = AgilePortafolio()
        agile_metrics = agile_portafolio.collect_agile_metrics()
        for metric in agile_metrics:
            serializer.logger.write(metric, DATA_PATH)

    except Exception as error:
        logger.error(str(error), exc_info=True)
        logger.error("Application closed due error")
        sys.exit(1)

    logger.info("Finished collection of agile-portafolio")
    sys.exit(0)


if __name__ == "__main__":
    main()
