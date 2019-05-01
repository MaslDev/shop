import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
django.setup()
print('email:')
email = str(input())
print('first name:')
first_name = str(input())
print('last name:')
last_name = str(input())
print('password:')
password = str(input())

from authentication.models import Admin
Admin.objects.create_user(email=email, first_name = first_name, last_name = last_name, password=password)

print('Congratulation')
