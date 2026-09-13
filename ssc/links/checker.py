from urllib.parse import urljoin
from html.parser import HTMLParser
from ssc.auth import load_cookies
from ssc.util import get_response


def get_unverified_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.links = []
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and not value.startswith('mailto:'):
                    url = urljoin(self.base_url, value)
                    self.links.append(url)


def code_in_valid_range(code):
    return code is not None and 200 <= code < 400


def validate_links(page_url, auth_input=None):
    headers = {'Cookie': load_cookies(auth_input)} if auth_input else {}

    results = []
    res = get_response(page_url, headers=headers)
    if hasattr(res, 'html'):
        html_content = res.get('html')
    else:
        print(f"Failed to load the page: {page_url}")
        return results

    parser = LinkParser(page_url)
    parser.feed(html_content)

    for link in set(parser.links):
        code = get_response(link, headers=headers).get('code')
        if code_in_valid_range(code):
            print(f'OK ({code}): {link}')
        else:
            print(f'BAD ({code}): {link}')
        results.append((link, code))

    return results
