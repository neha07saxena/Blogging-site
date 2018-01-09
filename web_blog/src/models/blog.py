__author__="Neha"
import datetime
from src.common.database import Database
from src.models.post import Post
import uuid

class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
            #else: date = datetime.datetime.strptime(date, "%d%m%Y")
            # string parse time to take input in DDMMYYYY format
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'author_id': self.author_id,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):   # searches by the blog id
        blog_data=Database.find_one(collection='blogs',
                                    query={'_id': id})
        return cls(**blog_data)  # same as author=blog_data['author'] and so on

    @classmethod
    def find_by_author(cls, author_id):
        blogs = Database.find('blogs', {'author_id': author_id})
        return [cls(**blog) for blog in blogs]   # returns blog objects for data in the blogs satisfying the query

    @classmethod
    def get_all_blogs(cls):
        blogs = Database.find('blogs',{})
        return [cls(**blog) for blog in blogs]