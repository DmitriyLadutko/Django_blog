from django.db import models
from django.contrib.auth.models import User

LIKE_CHOICES = (('Like', 'Like'),
                ('Unlike', 'Unlike'))


class Article(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Title post')
    body = models.TextField(verbose_name='Text post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author post', max_length=50, null=True,
                               blank=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    count_view = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Post', blank=True, null=True,
                                related_name='comment_article')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author comment', max_length=50, null=True,
                               blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    text_comment = models.TextField(verbose_name='Comment text')
    moderation = models.BooleanField(verbose_name='moderation', default=False)
