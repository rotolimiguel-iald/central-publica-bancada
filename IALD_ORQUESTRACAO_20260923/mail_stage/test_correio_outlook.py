"""Offline guard tests. No real Outlook calls or messages."""
import contextlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace as N
import unittest
from unittest.mock import patch
import uuid
import correio_outlook as m


class MailGuards(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.old = m.STATE
        m.STATE = Path(self.temp.name)
        self.account = N(SmtpAddress='sender@example.test')
        self.calls = 0
        self.mail = N(SendUsingAccount=self.account, To='target@example.test', CC='', BCC='',
                      Subject='Reviewed', Body='Approved text', Attachments=N(Count=0),
                      Recipients=[N(Type=1, Address='target@example.test')], Send=self.deliver)
        self.app = N(Session=N(Accounts=[self.account], GetItemFromID=lambda *a: self.mail))
        self.draft = str(uuid.uuid4())
        self.sha = m.fingerprint(self.mail, self.account.SmtpAddress)
        self.path = m.journal_path(self.account.SmtpAddress, self.draft)
        m.atomic_json(self.path, dict(draft_id=self.draft, sender=self.account.SmtpAddress,
                                     entry_id='item', store_id='store', sha256=self.sha,
                                     state='DRAFT_REVIEW_REQUIRED'))
        self.req = dict(sender=self.account.SmtpAddress, draft_id=self.draft,
                        confirmed=True, expected_sha256=self.sha)
        self.patcher = patch.object(m, 'active_outlook', lambda: contextlib.nullcontext(self.app))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        m.STATE = self.old
        self.temp.cleanup()

    def deliver(self):
        self.calls += 1

    def test_unknown_sender_has_no_default_fallback(self):
        with self.assertRaises(ValueError):
            m.choose_account([self.account], 'other@example.test')

    def test_duplicate_sender_is_ambiguous(self):
        with self.assertRaises(ValueError):
            m.choose_account([self.account, self.account], self.account.SmtpAddress)

    def test_confirmation_required(self):
        self.req['confirmed'] = False
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 0)

    def test_body_change_requires_review(self):
        self.mail.Body += ' altered'
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 0)

    def test_recipient_change_requires_review(self):
        self.mail.Recipients[0].Address = 'other@example.test'
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 0)

    def test_sender_change_blocks_send(self):
        self.mail.SendUsingAccount = N(SmtpAddress='other@example.test')
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 0)

    def test_review_hash_must_match(self):
        self.req['expected_sha256'] = 'wrong'
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 0)

    def test_send_once_not_delivery_claim(self):
        result = m.send(self.req)
        self.assertFalse(result['delivery_confirmed'])
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 1)

    def test_uncertain_send_not_retried(self):
        def fail():
            self.calls += 1
            raise RuntimeError('Transport failure')
        self.mail.Send = fail
        with self.assertRaises(RuntimeError):
            m.send(self.req)
        with self.assertRaises(ValueError):
            m.send(self.req)
        self.assertEqual(self.calls, 1)
        self.assertEqual(json.loads(self.path.read_bytes())['state'], 'SUBMISSION_STARTED_UNCERTAIN')

    def test_header_injection_rejected(self):
        with self.assertRaises(ValueError):
            m.address('sender@example.test\r\nBcc: other@example.test')

    def test_no_body_in_receipt(self):
        self.assertNotIn(self.mail.Body, self.path.read_text())


if __name__ == '__main__':
    unittest.main()
