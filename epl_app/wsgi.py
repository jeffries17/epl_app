import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = get_wsgi_application()
