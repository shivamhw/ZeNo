class User:
    def __init__(self, name):
        self.username = name
        self.password = None
        self.jwt_token = None
        self.cookie = None
        self.cs_token = None

