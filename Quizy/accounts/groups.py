from django.contrib.auth.models import Group, Permission

superuser_group, _ = Group.objects.get_or_create(name='Superuser')
staff_group, _ = Group.objects.get_or_create(name='Staff')

all_permissions = Permission.objects.all()

superuser_group.permissions.set(all_permissions)

staff_permissions = all_permissions.filter(content_type__model__in=['category', 'question'], codename__in=['add', 'change'])
staff_group.permissions.set(staff_permissions)
