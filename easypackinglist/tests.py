from django.core import mail
from django.test import TestCase
from django.conf import settings

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'The Easiest Packing List', 'This is a simple test message.',
            settings.EMAIL_HOST_USER, ['alex@passportcreative.co'],
            fail_silently=False,
        )


        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct
        self.assertEqual(mail.outbox[0].subject, 'The Easiest Packing List')
