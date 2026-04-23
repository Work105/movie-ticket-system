from django.db import migrations

def create_shared_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'CustomUser')
    
    if not User.objects.filter(username='tharaka').exists():
        User.objects.create_superuser(
            username='tharaka',
            email='tharaka@example.com',
            password='tara123',
            role='admin'
        )
        print("✅ Shared admin created: tharaka / tara123")

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0002_remove_movie_poster_movie_poster_url'),
    ]

    operations = [
        migrations.RunPython(create_shared_admin),
    ]