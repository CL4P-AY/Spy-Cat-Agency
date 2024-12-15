import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spy_cat_agency_test_task.settings")

application = get_asgi_application()
