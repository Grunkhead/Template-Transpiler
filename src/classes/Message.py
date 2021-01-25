


class Message:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def fail(cls, message):
        print(cls.FAIL + message + cls.ENDC)

    @classmethod
    def warning(cls, message):
        print(cls.WARNING + message + cls.ENDC)

    @classmethod
    def success(cls, message):
        print(cls.GREEN + message + cls.ENDC)

    @classmethod
    def advice(cls, message):
        print(cls.BLUE + message + cls.ENDC)
        