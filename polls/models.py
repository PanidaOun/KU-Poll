"""models for polls project."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Class that has a question and a publication date."""
    previous_vote = models.CharField(max_length=200, default="")
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('Ending date')

    def __str__(self):
        """Def to return a question text."""
        return self.question_text

    def was_published_recently(self):
        """Def to return the day that question published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Def to return boolean to show that question published or not."""
        current_date = timezone.now()
        if (current_date >= self.pub_date):
            return True
        return False

    def can_vote(self):
        """Def to return boolean to show that user can vote or not."""
        current_date = timezone.now()
        if (current_date >= self.pub_date and current_date < self.end_date):
            return True
        return False


class Choice(models.Model):
    """Class that has two fields:the text of choice and a vote tally."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Def to return a choice text."""
        return self.choice_text

class Vote(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)