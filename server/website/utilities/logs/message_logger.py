class Logger:
    def __init__(self, log):
        self.log = log + "_log.txt"

    def __call__(self, message):
        self.add(message)

    def add(self, message):
        log = ",".join([str(message[key]) for key in message])
        file = open(self.log, "a")
        file.write(log)
        file.write("\n")
        file.close()

    def get(self, message):
        log = ",".join([str(message[key]) for key in message])
        for line in open(self.log):
            if line.strip("\n") == log:
                return True
        return False

    def topic_exists(self, topic):
        for line in open(self.log):
            log = set(line.strip("\n").split(","))
            if topic in log:
                return True
        return False
