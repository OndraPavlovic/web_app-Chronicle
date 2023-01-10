import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Record


class RecordModelTests(TestCase):

    def test_was_published_recently_with_future_record(self):
        """
        was_published_recently() returns False for records whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_record = Record(pub_date=time)
        self.assertIs(future_record.was_published_recently(), False)

    def test_was_published_recently_with_old_record(self):
        """
        was_published_recently() returns False for records whose pub_date
        is older than 7 days.
        """
        time = timezone.now() - datetime.timedelta(days=7, seconds=1)
        old_record = Record(pub_date=time)
        self.assertIs(old_record.was_published_recently(), False)

    def test_was_published_recently_with_recent_record(self):
        """
        was_published_recently() returns True for records whose pub_date
        is within the last 7 days.
        """
        time = timezone.now() - datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
        recent_record = Record(pub_date=time)
        self.assertIs(recent_record.was_published_recently(), True)


def create_record(title, days):
    """
    Create a record with the given `title` and published the
    given number of `days` offset to now (negative for records published
    in the past, positive for records that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Record.objects.create(title=title, pub_date=time, start_date=timezone.now(), end_date=timezone.now())


class RecordIndexViewTests(TestCase):
    def test_no_records(self):
        """
        If no records exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('chronicle:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No records are available.")
        self.assertQuerysetEqual(response.context['latest_record_list'], [])

    def test_past_record(self):
        """
        Record with a pub_date in the past are displayed on the
        index page.
        """
        record = create_record(title="Past record.", days=-30)
        response = self.client.get(reverse('chronicle:index'))
        self.assertQuerysetEqual(
            response.context['latest_record_list'],
            [record],
        )

    def test_future_record(self):
        """
        Records with a pub_date in the future aren't displayed on
        the index page.
        """
        create_record(title="Future record.", days=30)
        response = self.client.get(reverse('chronicle:index'))
        self.assertContains(response, "No records are available.")
        self.assertQuerysetEqual(response.context['latest_record_list'], [])

    def test_future_record_and_past_record(self):
        """
        Even if both past and future records exist, only past records
        are displayed.
        """
        record = create_record(title="Past record.", days=-30)
        create_record(title="Future record.", days=30)
        response = self.client.get(reverse('chronicle:index'))
        self.assertQuerysetEqual(
            response.context['latest_record_list'],
            [record],
        )

    def test_two_past_records(self):
        """
        The records index page may display multiple records.
        """
        record1 = create_record(title="Past record 1.", days=-30)
        record2 = create_record(title="Past record 2.", days=-15)
        response = self.client.get(reverse('chronicle:index'))
        self.assertQuerysetEqual(
            response.context['latest_record_list'],
            [record2, record1],
        )


class RecordDetailViewTests(TestCase):
    def test_future_record(self):
        """
        The detail view of a record with a pub_date in the future
        returns a 404 not found.
        """
        future_record = create_record(title='Future record.', days=5)
        url = reverse('chronicle:detail', args=(future_record.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_record(self):
        """
        The detail view of a record with a pub_date in the past
        displays the record's text.
        """
        past_record = create_record(title='Past record.', days=-5)
        url = reverse('chronicle:detail', args=(past_record.id,))
        response = self.client.get(url)
        self.assertContains(response, past_record.title)
