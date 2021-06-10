from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

'''
 Django docs define models the following way:
        A model is the single, definitive source of information about your data. 
        It contains the essential fields and behaviors of the data you’re storing. 
        Generally, each model maps to a single database table.
 Each model can be constructed with a class, where each attribute is a field in the model stored in a database.
'''

class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=2048)
    image = models.ImageField(upload_to='uploads/post/', blank=True)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=1024)
    pub_date = models.DateField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='related post', default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', default=0)

    def __str__(self):
        return f'{self.author}\'s comment'
