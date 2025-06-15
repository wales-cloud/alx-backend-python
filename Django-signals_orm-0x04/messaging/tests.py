# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='alicepwd')
        self.receiver = User.objects.create_user(username='bob', password='bobpwd')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello Bob!')
        notif = Notification.objects.get(message=msg)
        self.assertEqual(notif.user, self.receiver)
