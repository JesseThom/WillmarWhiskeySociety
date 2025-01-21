from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE, bcrypt

class User:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.name = data['name']
        self.password = data['password']

#register validation
    # @staticmethod
    # def validate(data):
    #     is_valid = True
    #     pwd = data["password"]
    #     temp_pwd = data['confirm_password']

    #     if len(data["name"]) < 3:
    #         flash("Name must be at least 3 characters.","err_users_name")
    #         is_valid=False
    #     else:
    #         temp_user = User.get_one_by_name({'name':data['name']})
    #         if temp_user:
    #             flash("Name already exhist","err_users_name")
    #             is_valid=False

    #     if len(pwd) < 5:
    #         flash("Password must be at least 5 characters.","err_users_password")
    #         is_valid=False

    #     if pwd != temp_pwd:
    #         flash("Passwords do not match","err_passwords_match")
    #         is_valid=False

    #     return is_valid

#login validation
    @staticmethod
    def validate_login(data,user):
        is_valid = True

        if not user:
            flash("Name is not reristered","err_users_login")
            is_valid = False
        else:
            password_check = bcrypt.check_password_hash(user.password, data['password'])
            if not password_check:
                flash ("Incorrect Password","err_users_login_pw")
                is_valid = False

        if len(data["password"]) < 5:
            flash("Password must be at least 5 characters.","err_users_login_pw")
            is_valid=False

        return is_valid
    
#C
    # @classmethod
    # def create(cls,data):
    #     #1 query statement
    #     query = "INSERT INTO users (name, password) VALUES (%(name)s,%(password)s);"
    #     #2 contact the data
    #     user_id = connectToMySQL(DATABASE).query_db(query, data) 
    #     return user_id
    
#R
    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s;"
    #     #returns list of dictionaries
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     # print(results)
        
    #     if not results:
    #         return False
        
    #     return cls(results[0])
    
    @classmethod
    def get_one_by_name(cls, data):
        query = "SELECT * FROM users WHERE name = %(name)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        
        if not results:
            return False
        
        return cls(results[0])

#     @classmethod
#     def get_all(cls):
#         query = "SELECT * FROM users"
#         results = connectToMySQL(DATABASE).query_db(query)
#         all_users = []
#         for dict in results:
#             all_users.append(cls(dict))
#         return all_users
    
# #U
#     @classmethod
#     def update_one(cls,data):
#         query = "UPDATE users SET first_name = %(name)s, WHERE id = %(id)s;"
#         return connectToMySQL(DATABASE).query_db(query,data)
    
# #D
#     @classmethod
#     def delete_one(cls,data):
#         query = "DELETE FROM users WHERE id = %(id)s;"
#         return connectToMySQL(DATABASE).query_db(query,data)