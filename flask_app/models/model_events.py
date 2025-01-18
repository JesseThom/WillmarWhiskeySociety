from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

# class Event:
#     def __init__(self,data:dict):
#         self.id = data['id']
#         self.title = data['title']
#         self.date = data['date']
#         self.location = data['location']
#         self.description = data['description']
#         self.address = data['address']
#         self.about_1 = data['about_1']
#         self.pic_location = data['pic_location']
#         self.history = data['history']

class Event:
    def __init__(self,data:dict):
        self.id = data.get('id')
        self.title = data.get('title','')
        self.date = data.get('date','')
        self.location = data.get('location','')
        self.description = data.get('description','')
        self.address = data.get('address','')
        self.about_1 = data.get('about_1','')
        self.about_2 = data.get('about_2','')
        self.pic_location = data.get('pic_location','')
        self.history = data.get('history','')
        self.tickets_url = data.get('tickets_url','')

#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO events (id, title, date, location, description, address, about_1, about_2, pic_location, tickets_url) VALUES (%(id)s,%(title)s,%(date)s,%(location)s,%(description)s,%(address)s,%(about_1)s,%(about_2)s,%(pic_location)s,%(tickets_url)s);"
        #2 contact the data
        team_id = connectToMySQL(DATABASE).query_db(query, data) 
        return team_id
#R    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events ORDER BY id ASC;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_events = []
        for dict in results:
            all_events.append(cls(dict))
        return all_events
    
    @classmethod
    def get_all_current(cls):
        query = "SELECT * FROM events WHERE history = 0 ORDER BY id ASC;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_events = []
        for dict in results:
            all_events.append(cls(dict))
        return all_events
    
    @classmethod
    def get_all_history(cls):
        query = "SELECT events.id, events.title, events.pic_location, events.about_2 FROM events WHERE history = 1 ORDER BY id DESC;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_events = []
        for dict in results:
            all_events.append(cls(dict))
        return all_events
    
#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE events SET id = %(id)s, pic_location = %(pic_location)s, title = %(title)s, description = %(description)s, location = %(location)s, address = %(address)s, date = %(date)s, about_1 = %(about_1)s, about_2 = %(about_2)s, history = %(history)s, tickets_url = %(tickets_url)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
# #D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)