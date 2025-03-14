import urllib.request
from urllib.parse import urljoin
from html.parser import HTMLParser


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


def check_url(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.getcode()
    except Exception as e:
        print(f'Error checking {url}: {e}')
        return None


def validate_links(page_url):
    results = []
    try:
        with urllib.request.urlopen(page_url) as response:
            html_content = response.read().decode()
    except Exception as e:
        print(f'Error loading page {page_url}: {e}')
        return results

    parser = LinkParser(page_url)
    parser.feed(html_content)

    valid_codes = range(200, 400)
    for link in set(parser.links):
        code = check_url(link)
        if code in valid_codes:
            print(f'OK ({code}): {link}')
        elif code:
            print(f'BAD ({code}): {link}')
        results.append((link, code))

    return results
