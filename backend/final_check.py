import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Check users
sekiro_exists = User.objects.filter(username='Sekiro').exists()
trial12_exists = User.objects.filter(username='trial12').exists()

print(f"Sekiro Exists: {sekiro_exists}")
print(f"trial12 Exists: {trial12_exists}")
