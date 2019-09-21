import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/grader/Item-Catalog")
from app import app as application
application.root_path = '/home/grader/Item-Catalog'