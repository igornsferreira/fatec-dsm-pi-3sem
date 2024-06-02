from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacaomodel',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
