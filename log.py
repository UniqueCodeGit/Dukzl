import logging

FORMATTER = logging.Formatter(
    "[%(levelname)s][%(name)s][%(asctime)s]: %(message)s"
)

class Logger:
    @staticmethod
    def basicLogger(cog):
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
    def discordLogger():
        logger = logging.getLogger('discord')
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