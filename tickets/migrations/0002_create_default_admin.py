from django.db import migrations

def create_default_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Default admin user created: admin / admin123")
    else:
        print("⚠️ Admin user already exists")

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0001_initial'),  # Change this to your last migration number
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]