# your_app/migrations/000X_auto_YYYYMMDD_HHMM.py

from django.db import migrations

def create_vector_extension(apps, schema_editor):
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

class Migration(migrations.Migration):

    dependencies = [
        ('app_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_vector_extension),
    ]
