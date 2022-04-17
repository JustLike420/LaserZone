from django.db import models


# Create your models here.
class Post(models.Model):
    post_id = models.IntegerField(default=0)
    text = models.TextField(verbose_name="text")
    data = models.DateField()
    photo = models.ImageField(default='news-3.jpg')

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
