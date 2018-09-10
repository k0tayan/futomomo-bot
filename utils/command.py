class CommandHandler:
    def __init__(self):
        pass

class CommandChecker:
    def __init__(self):
        pass

    def include_command(self, string, commands):
        for command in commands:
            if command in string:
                return True
        return False
