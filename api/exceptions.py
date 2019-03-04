class NotAuthorized(Exception):
    def __init__(self, data):
        self.data = data