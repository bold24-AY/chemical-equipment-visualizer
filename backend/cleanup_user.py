import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Delete Sekiro
try:
    u = User.objects.get(username='Sekiro')
    u.delete()
    print("Successfully deleted user 'Sekiro'.")
except User.DoesNotExist:
    print("User 'Sekiro' not found.")

# Verify trial12 exists
if User.objects.filter(username='trial12').exists():
    print("User 'trial12' exists and is preserved.")
else:
    print("WARNING: User 'trial12' NOT found!")
