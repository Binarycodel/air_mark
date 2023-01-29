import re

class Validator:
    def __init__(self):
        pass

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone):
        pattern = r'^\+?\d{10,15}$'
        return re.match(pattern, phone) is not None

    
    