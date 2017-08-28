from app import db
import datetime
from flask import url_for




class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name=u"Коментар", required=True)
    author = db.StringField(verbose_name=u"Ім'я", max_length=255, required=True)


class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(verbose_name=u"Заголовок", max_length=255, required=True)
    slug = db.StringField(verbose_name=u"Слаг", max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug', "$title"],
        'default_language': 'russian',
        'weights': {'title': 10},
        'ordering': ['-created_at']
    }


class BlogPost(Post):
    body = db.StringField(verbose_name=u"Текст", required=True)
    embed_code = db.StringField(verbose_name=u"Ембед код")
    image_url = db.StringField(verbose_name=u"URL картинки", max_length=255)
    image_url_second = db.StringField(verbose_name=u"URL картинки", max_length=255)
    author = db.StringField(verbose_name=u"Ім'я автора", max_length=255)



class Video(Post):
    embed_code = db.StringField(verbose_name=u"Ембед код",required=True)


class Image(Post):
    image_url = db.StringField(verbose_name=u"URL картинки",required=True, max_length=255)


class Quote(Post):
    body = db.StringField(verbose_name=u"Цитата",required=True)
    author = db.StringField(verbose_name=u"Ім'я", required=True, max_length=255)
