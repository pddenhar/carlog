#!/usr/bin/python
# Run a test server.
from web_apps import wsgi
application = wsgi.WebApp("app")
application.run(host='0.0.0.0', port=8080, debug=True)