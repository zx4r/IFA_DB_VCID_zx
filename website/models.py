
##Design der SQL DB
class Note:
    def __init__(self, id, data, date, user_id):
        self.id = id
        self.data = data
        self.date = date
        self.user_id = user_id

class User:
    def __init__(self, id, email, password, firstname):
        self.id = id
        self.email = email
        self.password = password
        self.firstname = firstname
        
