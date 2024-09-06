from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator 

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length = 50, null = True)
    email = models.EmailField(max_length = 100, null = True)

    def __str__ (self):
        return self.name
    
class Tag(models.Model):
    caption = models.CharField(max_length = 30)

    def __str__(self): 
        return self.caption  

class Post(models.Model):
    title = models.CharField(max_length = 50)
    excerpt = models.CharField(max_length = 100)
    # image_name = models.CharField(max_length = 30)
    image = models.ImageField(upload_to = "posts", null = True)
    date = models.DateField(auto_now = True)
    slug = models.SlugField(unique = True, db_index = True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete = models.SET_NULL,related_name = "posts", null = True)
    tags = models.ManyToManyField(Tag, related_name = "posts")


    def data(self):
        return f"{self.title} {self.date}"

    def __str__(self):
        return self.data()


class Comment(models.Model):
    user_name = models.CharField(max_length=127)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text


