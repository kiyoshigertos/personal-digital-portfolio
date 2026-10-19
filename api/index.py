import os
import sys

# Ensure project root directory is on the Python module search path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the WSGI Flask application instance for Vercel Serverless Function runtime
from app import app

class VercelPathMiddleware:
    """
    WSGI middleware that strips Vercel rewrite prefixes (/api/index or /api/index.py)
    from PATH_INFO so that Flask matches the intended routes (e.g., '/', '/projects').
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for prefix in ('/api/index.py', '/api/index'):
            if path == prefix:
                environ['PATH_INFO'] = '/'
                break
            elif path.startswith(prefix + '/'):
                environ['PATH_INFO'] = path[len(prefix):]
                break
        return self.wsgi_app(environ, start_response)

# Apply WSGI middleware
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

