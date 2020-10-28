import datetime

from django.test import TestCase
from django.utils import timezone
from polls.models import Question



class QuestionModelTests(TestCase):
    """Class for test about question."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_current_date_after_pub_date(self):
        """is_published() returns True if current date is after question’s publication date."""
        time = timezone.now() - datetime.timedelta(days=1)
        before = Question(pub_date=time)
        self.assertIs(before.is_published(), True)

    def test_is_published_current_date_on_pub_date(self):
        """is_published() returns True if current date is on question’s publication date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        now = Question(pub_date=time)
        self.assertIs(now.is_published(), True)

    def test_is_published_current_date_before_pub_date(self):
        """is_published() returns False if current date is before question’s publication date."""
        time = timezone.now() + datetime.timedelta(days=30)
        after = Question(pub_date=time)
        self.assertIs(after.is_published(), False)

    def test_can_vote_before_end_date(self):
        """can_vote returns True if current date is after pub_date and before end_date."""
        pub_time = timezone.now() - datetime.timedelta(days=3)
        end_time = pub_time + datetime.timedelta(days=5)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """can_vote returns False if current date is after end_date."""
        pub_time = timezone.now() - datetime.timedelta(days=10)
        end_time = pub_time + datetime.timedelta(days=5)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote() return False for questions whose pub_date is in the future.."""
        pub_time = timezone.now() + datetime.timedelta(days=10)
        end_time = pub_time + datetime.timedelta(days=10)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), False)
