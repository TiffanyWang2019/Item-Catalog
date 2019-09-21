import sys
import logging
import site
activatethis = '/home/grader/Item-Catalog/venv/bin/activate_this.py'
exec(compile(open(activatethis, "rb").read(), activatethis, 'exec'), globals, locals)
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/grader/Item-Catalog/scripts")
from app import app as application
application.secret_key = 'development'
site_packages = '/home/grader/.local/lib/python3.6/site-packages'
site.addsitedir(site_packages)
