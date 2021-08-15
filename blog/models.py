from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class PostCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            blank=True, null=True, related_name='children')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category', blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Post(models.Model):
    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='post_category')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    tags = TaggableManager()
    image = models.ImageField(upload_to='posts')
    status = models.CharField(max_length=20, choices=POST_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})
