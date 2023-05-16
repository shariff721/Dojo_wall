from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
    DB = "twitter_DB"

    def __init__(self,data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.owner = None

    @classmethod
    def save_post(cls,data):
        query = """
            INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    @classmethod
    def get_all_posts(cls):
        query = """SELECT * FROM posts;"""
        results = connectToMySQL(cls.DB).query_db(query)
        all_posts = []
        for one_post in results:
            all_posts.append(cls(one_post))
        return all_posts
    
    @classmethod
    def delete_post(cls,data):
        query = """
            DELETE FROM posts WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_all_posts_with_owner(cls):
        query = """
            SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_posts = []
        for row in results:
            one_post = cls(row)

            one_post_owner = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"]
            }
            owner = user.User(one_post_owner)
            one_post.owner = owner

            all_posts.append(one_post)
        return all_posts
    
    @staticmethod
    def validate_post(post):
        is_valid = True

        if len(post["content"]) <= 0:
            flash(" Post Content Must Not be blank","post")
            is_valid = False
        return is_valid



        
