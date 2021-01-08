import os

class GenerelUtils:
    @staticmethod
    def AutoCommands(bot):
        command_list = os.listdir("cogs/")
        for i in command_list:
            if i.endswith(".py"):
                command_name = "cogs." + i.replace(".py", "")
                bot.load_extension(command_name)

    @staticmethod
    def AutoCommandsReload(bot):
        command_list = os.listdir("cogs/")
        command_list = [
            command for command in command_list if command.endswith(".py")
            ]
        for i in command_list:
            command_name = "cogs." + i.replace(".py", "")
            try:
                bot.reload_extension(command_name)
            except Exception: pass

    @staticmethod
    def AutoCommandsload(bot):
        command_list = os.listdir("cogs/")
        command_list = [
            command for command in command_list if command.endswith(".py")
            ]
        for i in command_list:
            command_name = "cogs." + i.replace(".py", "")
            try:
                bot.load_extension(command_name)
            except Exception: pass


    @staticmethod
    def AutoCommandsunload(bot):
        command_list = os.listdir("cogs/")
        command_list = [
            command for command in command_list if command.endswith(".py")
            ]
        for i in command_list:
            command_name = "cogs." + i.replace(".py", "")
            try:
                bot.unload_extension(command_name)
            except Exception: pass