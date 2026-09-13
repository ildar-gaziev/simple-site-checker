import unittest
import os
import tempfile
from ssc.auth.auth import load_cookies

class TestAuth(unittest.TestCase):
    def test_load_cookies_from_string(self):
        cookie_string = "session=12345"
        result = load_cookies(cookie_string)
        self.assertEqual(result, cookie_string)

    def test_load_cookies_from_file(self):
        cookie_string = "session=abcdef"
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(cookie_string)
            temp_path = f.name
            
        try:
            result = load_cookies(temp_path)
            self.assertEqual(result, cookie_string)
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
