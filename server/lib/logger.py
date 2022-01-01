from lib.chronos import Chronos

class Log:
    def __init__(self, filename):
        self.__filename = filename

    def log(self, msg, stdout=False):
        if stdout:
            print(msg)

        with open(self.__filename, "a") as file:
            file.write("[%s]: %s\n" % (Chronos.now_str(), msg))
