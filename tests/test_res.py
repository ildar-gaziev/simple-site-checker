import unittest
from ssc.util.res import get_response


class TestLinkChecker(unittest.TestCase):

    def test_check_good_url_code(self):
        res = get_response('https://www.example.com')
        self.assertIn(res.get('code'), range(200, 400))

    def test_link_bad_code(self):
        res = get_response('https://example.com/non-existing-url')
        self.assertEqual(res.get('code'), 404)


if __name__ == '__main__':
    unittest.main()
