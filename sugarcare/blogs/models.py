from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model


class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})
    

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=13)
    content=models.TextField(max_length=255)

    def __str__(self):
        return 'Message from '+self.name
    

class Comments(models.Model):
    post= models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment=models.CharField(max_length=150)
    author= models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('bloghome')
    


    
    


