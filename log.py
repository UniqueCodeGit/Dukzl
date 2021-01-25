import logging

FORMATTER = logging.Formatter("[%(levelname)s][%(name)s][%(asctime)s]: %(message)s")


class Log:
    @staticmethod
    def cogLogger(cog) -> logging.Logger:
        name = cog.__class__.__qualname__
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(FORMATTER)
            filehandler = logging.FileHandler(f"logs/{name}.txt", "a")
            filehandler.setFormatter(FORMATTER)
            logger.addHandler(streamhandler)
            logger.addHandler(filehandler)

        logger.info(f"{name} Loaded.")
        return logger

    @staticmethod
    def defaultLogger(name) -> logging.Logger:
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)

        if not log.hasHandlers():
            stream_handler = logging.StreamHandler()
            filehandler = logging.FileHandler("logs/{}.txt".format(name), "a")
            stream_handler.setFormatter(FORMATTER)
            filehandler.setFormatter(FORMATTER)
            log.addHandler(filehandler)
            log.addHandler(stream_handler)

        log.info(f"{name} Loaded.")
        return log

    @staticmethod
    def discordLogger() -> logging.Logger:
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(FORMATTER)
            filehandler = logging.FileHandler(f"logs/discord.txt", "a")
            filehandler.setFormatter(FORMATTER)
            logger.addHandler(streamhandler)
            logger.addHandler(filehandler)

        logger.info(f"Discord Loaded.")
        return logger
