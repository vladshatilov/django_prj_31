from django.contrib.auth.models import AbstractUser
from django.db import models

# from ads.models import City


class Profile(AbstractUser):
    ROLES = [('member', "Member"), ("admin", "Admin")]
    role = models.CharField(max_length=15, default='member', choices=ROLES)
    birth_date = models.DateField(blank=False, null=False)
    email = models.EmailField()
    # age = models.PositiveSmallIntegerField(blank=True, null=True)
    # locations = models.ManyToManyField(City)
    #
    # class Meta:
    #     ordering = ["username"]
    #     verbose_name = 'Юзер'
    #     verbose_name_plural = 'Юзеры'

    # def __str__(self):
    #     return self.username
