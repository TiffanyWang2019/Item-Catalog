import sys
import logging
import site
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/grader/Item-Catalog")
from app import app as application
application.secret_key = 'development'
    
