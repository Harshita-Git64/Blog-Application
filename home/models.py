from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

    


class BlogPost(models.Model):
    
    title=models.CharField(max_length=255)
    #author=models.CharField(max_length=14)
    author= models.ForeignKey(User, on_delete=models.CASCADE,db_constraint=False)
    slug=models.CharField(max_length=130)
    content=models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime=models.DateTimeField(auto_now_add=True)
    
    ''' def __str__(self):
        return self.title + " by " + self.author'''
    
    def get_absolute_url(self):
      return reverse('blog')
    
class Comment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    

