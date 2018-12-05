ADMIN = 100
ADMINISTRATOR = ["Uc45442e19e3f8326fc321e828003f710", "U1e73ade0030068a7f41e05e72fd54418"]
class CommandHandler:
    def __init__(self):
        pass

class CommandChecker:
    def __init__(self):
        pass

    def check_authrity(self, user_id):
        if user_id in ADMINISTRATOR:
            return True
        else:
            return  False

    def include_command(self, string, commands):
        for command in commands:
            if command in string:
                return True
        return False
