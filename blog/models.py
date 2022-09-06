from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

STATUS = ((0, "Draft"), (1, "Published"))

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='blog\images')
    # slug = models.SlugField(max_length=200, default="blog")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'blog_posts', default=1)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    is_best = models.BooleanField("Blog hay", default=False)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS, default=1)
    tags = TaggableManager()
    # date = models.DateField()
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title
# Create your models here.
