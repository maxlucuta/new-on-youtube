PATH = "./website/utilities/pubsub/logs/"


class Logger:
    """Logging class to allow for 0 to 1 messaging with
       Google PubSub."""

    def __init__(self, log: str):
        """Constructs a Logger object.

        Args:
            log (str): name of logger to access,
            either publisher or subscriber
        """

        self.log = PATH + log + "_log.txt"

    def __call__(self, message: str):
        """Calls self.add, see below documentation.

        Args:
            message (str): message to log
        """

        self.add(message)

    def add(self, message: str):
        """Writes a message to the specified log file.

        Args:
            message (str): message to log
        """

        file = open(self.log, "a")
        file.write(message)
        file.write("\n")
        file.close()

    def get(self, message: str) -> bool:
        """Checks if a message exists in one of the log
           files.

        Args:
            message (str): message to lookup

        Returns:
            bool: True if message exists, false otherwise
        """

        for line in open(self.log):
            if line.strip("\n") == message:
                return True
        return False

    def topic_exists(self, topic: str) -> bool:
        """Checks if a topic exists in one of the log
           files.

        Args:
            message (str): topic to lookup

        Returns:
            bool: True if topic exists, false otherwise
        """

        for line in open(self.log):
            log = set(line.strip("\n").split(","))
            if topic in log:
                return True
        return False
