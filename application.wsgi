import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/grader/Item-Catalog")
sys.path.insert(0,"/home/grader/Item-Catalog/scripts")
from app import app as application
application.secret_key = 'development'