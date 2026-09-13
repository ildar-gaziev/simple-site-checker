import urllib.request
import urllib.error
import ssl

def get_response(url, headers=None, method='GET'):
    """
    Sends an HTTP request to the given URL and returns the response code and HTML content (if GET).
    
    Args:
        url (str): The URL to request.
        headers (dict): Optional HTTP headers to include.
        method (str): HTTP method to use (e.g., 'GET', 'HEAD').
        
    Returns:
        dict: A dictionary containing 'code' (int) and optionally 'html' (str), or an error 'msg' (str).
    """
    try:
        req = urllib.request.Request(url, headers=headers or {}, method=method)
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            result = {'code': response.getcode()}
            if method.upper() == 'GET':
                result['html'] = response.read().decode('utf-8', errors='ignore')
            return result
    except urllib.error.HTTPError as e:
        print(f'HTTP error for {url}: {e.code}')
        return {'code': e.code, 'msg': f'HTTP error for {url}: {e.code}'}
    except urllib.error.URLError as e:
        print(f'URL error for {url}: {e.reason}')
        return {'msg': f'URL error for {url}: {e.reason}'}
    except Exception as e:
        print(f'Unexpected error for {url}: {e}')
        return {'msg': f'Unexpected error for {url}: {e}'}
