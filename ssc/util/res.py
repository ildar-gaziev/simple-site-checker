import urllib.request
import urllib.error
import ssl

def get_response(url, headers=None):
    try:
        req = urllib.request.Request(url, headers=headers or {})
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=50, context=ctx) as response:
            return {'html': response.read().decode('utf-8'), 'code': response.getcode()}
    except urllib.error.HTTPError as e:
        print(f'HTTP error for {url}: {e.code}')
        return {'code': e.code, 'msg': f'HTTP error for {url}: {e.code}'}
    except urllib.error.URLError as e:
        print(f'URL error for {url}: {e.reason}')
        return {'msg': f'URL error for {url}: {e.reason}'}
    except Exception as e:
        print(f'Unexpected error for {url}: {e}')
        return {'msg': f'Unexpected error for {url}: {e}'}
