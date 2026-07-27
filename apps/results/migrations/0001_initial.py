from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserTestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField(default=0)),
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
