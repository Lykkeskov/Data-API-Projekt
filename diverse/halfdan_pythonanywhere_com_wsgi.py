# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below was written by Tobias and may not work.

import sys
path = '/home/halfdan/mywebapp'
if path not in sys.path:
    sys.path.append(path)

from flask_app import app as application
