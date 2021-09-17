from datetime import timedelta, time, datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model


today = timezone.now()
tomorrow = today + timedelta(1)
yesterday = today - timedelta(1)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))
yesterday_start = make_aware(datetime.combine(yesterday, time()))


class Command(BaseCommand):
    help = "Welcome letter to a new user with a proposal to take the test"

    def handle(self, *args, **options):
        new_users = get_user_model().objects.filter(date_joined__range=(yesterday_start, today_start))

        if new_users:
            for user in new_users:
                if not user.results:
                    message = f"Welcome {user}. Thank you for registering. Perhaps you would like to take a couple of tests? "
                    subject = f"Welcome {user} "
                    send_mail(subject=subject, message=message, recipient_list=[user.email], html_message=None)
                    self.stdout.write(f"E-mail to {user} was sent.")
        else:
            self.stdout.write("No new users today.")
