from django import forms
from django.db import models
from django.contrib.auth.models import User
from accounts.forms import MyRegistrationForm
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

class Health(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Prefer Not to State', 'Prefer Not to State'))

    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200, default=None, choices=GENDER_CHOICES)
    mental = models.BooleanField(default=False, blank=False)
    food = models.BooleanField(default=False, blank=False)
    sleep = models.BooleanField(default=False, blank=False)
    exercise = models.BooleanField(default=False, blank=False)
    age = models.IntegerField(
        validators=[MinValueValidator(17), MaxValueValidator(80)],
        error_messages={
            "age":"The age requirement is between 17 and 80 years old."
        }
    )
    def __str__(self):
        return 'Age of {} is {}'.format(self.author, self.age)

class General(models.Model):

    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    thumbnail = models.ImageField(default="default.jpg", blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    ig = models.CharField(max_length=100, blank=True)
    fb = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    snap = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return 'Location of {} is {}'.format(self.author, self.location)

class Friend(models.Model):
    users = models.ManyToManyField(User)
    # look more into related_name
    # logined in user
    # null bc we don't have to have something or someone
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.SET_NULL)

# look more into the classmethod
    @classmethod
    def make_friend(cls, current_user, new_friend):
        # return an instance of friend
        friend, created = cls.objects.get_or_create(
            # check to see if the current object has that user as a friend
            current_user=current_user
        )

        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        # return an instance of friend
        friend, created = cls.objects.get_or_create(
            # check to see if the current object has that user as a friend
            current_user=current_user
        )
        friend.users.remove(new_friend)
