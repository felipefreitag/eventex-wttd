from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Fulano de Tal', cpf='01234567890',
                    email='ffvargas@gmail.com', phone='51 993711455')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """Email subject should be 'Confirmação de inscrição'"""
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Email sender should be contato@eventex.com.br"""
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """Should send an email to subscriber"""
        expect = ['contato@eventex.com.br', 'ffvargas@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        """Email body should have form information"""
        contents = ['Fulano de Tal',
                    '01234567890',
                    'ffvargas@gmail.com',
                    '51 993711455',
                    ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)