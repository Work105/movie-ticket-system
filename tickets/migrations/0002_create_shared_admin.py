from django.db import migrations

def create_shared_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    
    # Create shared admin account
    if not User.objects.filter(username='wathmini').exists():
        User.objects.create_superuser(
            username='wathmini',
            email='wathmini@example.com',
            password='wathmini123#'  # Change to your password
        )
        print("✅ Shared admin created: wathmini / wathmini123")
    else:
        print("⚠️ Admin already exists")

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_shared_admin),
    ]