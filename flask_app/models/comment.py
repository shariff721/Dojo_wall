from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, post

class Comment:
    DB = "twitter_DB"

    def __init__(self,data):
        self.post_id = data["post_id"]
        self.user_id = data["user_id"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.author = None

    @classmethod
    def save_comment(cls,data):
        query = """
            INSERT INTO comments (post_id, user_id, comment) VALUES (%(post_id)s, %(user_id)s, %(comment)s)
        """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    @classmethod
    def get_all_comments_with_owner(cls):
        query = """
            SELECT * FROM comments
            LEFT JOIN posts ON comments.post_id = posts.id
            LEFT JOIN users ON comments.user_id = users.id;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_comments = []
        for row in results:
            one_comment = cls(row)

            one_comment_owner = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
            }
            owner = user.User(one_comment_owner)
            one_comment.author = owner

            all_comments.append(one_comment)
        return all_comments