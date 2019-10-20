from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '--'.join(full_path[::-1])


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(default=None, unique=True)
    related_img = models.URLField(blank=True, null=True)
    text = RichTextField()
    short_description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    tags = TaggableManager(blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=30)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    def __str__(self):
        return self.text
