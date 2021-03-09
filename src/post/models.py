from datetime import date
from django_countries.fields import CountryField  # Прикрутил батарейку со странами

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

LIKE_CHOICES = (('Like', 'Like'),
                ('Unlike', 'Unlike'))

GENDER_CHOICES = (('male', 'male'),
                  ('female', 'female'),
                  ('european gender', 'european gender'))


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = CountryField(blank_label='Select country...')
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='media/', blank=True, null=True)

    def calculate_age(self):
        today = date.today()
        born = self.date_of_birth
        if today and born:
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return f'please input Date of Birth'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля автора при регистрации"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля автора при регистрации"""
    instance.profile.save()


class Category(models.Model):
    name = models.CharField('Category', max_length=150)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Title post')
    body = models.TextField(verbose_name='Text post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author post', max_length=50, null=True,
                               blank=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    count_view = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    draft = models.BooleanField(default=False)
    year = models.IntegerField(validators=[MinValueValidator(2021)], default=2021)

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


class GetCategory:
    @staticmethod
    def get_categories():
        return Category.objects.all()

    @staticmethod
    def get_year():
        return Article.objects.filter().values('year').distinct()
