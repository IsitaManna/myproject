# Generated by Django 3.0.2 on 2020-03-17 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('custID', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('fName', models.CharField(max_length=50)),
                ('lName', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=30)),
                ('contactNo', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('createdDate', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('questionID', models.AutoField(primary_key=True, serialize=False)),
                ('Question', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('responseID', models.AutoField(primary_key=True, serialize=False)),
                ('responseText', models.CharField(max_length=100)),
                ('questionID', models.ForeignKey(db_column='questionID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recommendationEngine.Questions')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageID', models.IntegerField(verbose_name=5)),
                ('rating', models.IntegerField(verbose_name=1)),
                ('email', models.ForeignKey(db_column='email', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recommendationEngine.Customer')),
            ],
        ),
    ]
