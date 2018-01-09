__author__="Neha"
import uuid
from src.common.database import Database
import datetime
class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):  #By default id is none, unless a value is there
        self.blog_id = blog_id
        self.created_date = created_date
        self.title = title
        self.content = content
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id  #uuid4 generates random id and hex gives a 32 char hexadec str

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'created_date': self.created_date,
            'title': self.title,
            'content': self.content,
            'author': self.author
        }

    @classmethod
    def from_mongo(cls, id):   #returns the data from a given id
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)  # equivalent to blog_id=post_data['blog_id'], and so on for all values

    @staticmethod
    def from_blog(id): #returns all posts for a blog id
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]