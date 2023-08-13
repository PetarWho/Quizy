from django.contrib.auth.models import Group, Permission

from Quizy.accounts.models import AppUser

superuser_group, _ = Group.objects.get_or_create(name='Superuser')
staff_group, _ = Group.objects.get_or_create(name='Staff')

all_permissions = Permission.objects.all()

superuser_group.permissions.set(all_permissions)

staff_permissions = all_permissions.filter(content_type__model__in=['category', 'question'], codename__in=['add', 'change'])
staff_group.permissions.set(staff_permissions)

user = AppUser
moderator_group, created = Group.objects.get_or_create(name='Moderator')
admin_group, created2 = Group.objects.get_or_create(name='Admin')

user.is_staff = True
user.save()
user.groups.add(moderator_group)

user.is_superuser = True
user.is_staff = True
user.save()
user.groups.add(admin_group)