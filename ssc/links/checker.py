from urllib.parse import urljoin, urlsplit, urlunsplit
from html.parser import HTMLParser
import concurrent.futures
from ssc.auth import load_cookies
from ssc.util import get_response


class LinkParser(HTMLParser):
    """
    Parses HTML content to extract all valid anchor tag links.
    """
    def __init__(self, base_url):
        super().__init__()
        self.links = []
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    if value.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
                        continue
                    url = urljoin(self.base_url, value)
                    parsed = urlsplit(url)
                    url_no_fragment = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ''))
                    self.links.append(url_no_fragment)


def code_in_valid_range(code):
    """
    Checks if the HTTP status code indicates a successful response (200-399).
    """
    return code is not None and 200 <= code < 400


def validate_links(page_url, auth_input=None):
    """
    Fetches the given page, extracts all unique links, and concurrently validates them.
    
    Args:
        page_url (str): The URL of the page to parse.
        auth_input (str): The path to a cookie file or a raw cookie string.
        
    Returns:
        list: A list of tuples containing (link, status_code).
    """
    headers = {'Cookie': load_cookies(auth_input)} if auth_input else {}

    results = []
    res = get_response(page_url, headers=headers)
    if 'html' in res:
        html_content = res.get('html')
    else:
        print(f"Failed to load the page: {page_url}")
        return results

    parser = LinkParser(page_url)
    parser.feed(html_content)

    def check_link(link):
        code = get_response(link, headers=headers, method='HEAD').get('code')
        if code_in_valid_range(code):
            print(f'OK ({code}): {link}')
        else:
            print(f'BAD ({code}): {link}')
        return (link, code)

    unique_links = set(parser.links)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_link, link): link for link in unique_links}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return results
