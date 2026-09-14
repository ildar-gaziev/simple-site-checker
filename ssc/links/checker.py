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


STRICT_DOMAINS = [
    'linkedin.com',
    'twitter.com',
    'x.com',
    'instagram.com',
    'facebook.com',
    'tiktok.com'
]


def get_link_status(code, url):
    """
    Evaluates the HTTP status code and returns a status string: 'OK', 'RESTRICTED', 'SKIPPED', or 'BAD'.
    - OK: 200-399 range, plus special cases like LinkedIn 999.
    - RESTRICTED: 403 (Forbidden), 429 (Too Many Requests), 503 (Service Unavailable) 
      which usually imply the link exists but blocks our bot.
    - SKIPPED: When the link was skipped by the user flag.
    - BAD: Everything else (e.g. 404, 500, None).
    """
    if code == 'SKIPPED':
        return 'SKIPPED'
        
    if code is None:
        return 'BAD'
        
    if 200 <= code < 400:
        return 'OK'
        
    if code in (403, 429, 503):
        return 'RESTRICTED'
        
    # Handle LinkedIn's specific 999 Request Denied anti-bot code
    if code == 999 and 'linkedin.com' in url:
        return 'OK'
        
    return 'BAD'


def is_strict_domain(link):
    try:
        netloc = urlsplit(link).netloc.lower()
        return any(netloc == d or netloc.endswith('.' + d) for d in STRICT_DOMAINS)
    except Exception:
        return False

def validate_links(page_url, auth_input=None, skip_strict=False):
    """
    Fetches the given page, extracts all unique links, and concurrently validates them.
    
    Args:
        page_url (str): The URL of the page to parse.
        auth_input (str): The path to a cookie file or a raw cookie string.
        skip_strict (bool): Skip validation for strict anti-bot domains.
        
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
        if skip_strict and is_strict_domain(link):
            code = 'SKIPPED'
        else:
            code = get_response(link, headers=headers, method='HEAD').get('code')
            
        status = get_link_status(code, link)
        print(f'{status} ({code}): {link}')
        return (link, code)

    unique_links = set(parser.links)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_link, link): link for link in unique_links}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Print statistics
    stats = {'OK': 0, 'RESTRICTED': 0, 'SKIPPED': 0, 'BAD': 0}
    for link, code in results:
        status = get_link_status(code, link)
        stats[status] += 1
        
    print("\n--- Validation Statistics ---")
    print(f"Total links checked: {len(results)}")
    print(f"OK: {stats['OK']}")
    print(f"RESTRICTED: {stats['RESTRICTED']}")
    print(f"SKIPPED: {stats['SKIPPED']}")
    print(f"BAD: {stats['BAD']}")
    print("-----------------------------\n")

    return results
