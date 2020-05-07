# Generated by Django 3.0.4 on 2020-05-07 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommendationEngine', '0018_merge_20200430_0521'),
    ]

    operations = [
        migrations.CreateModel(
            name='GANPredictImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.FileField(null=True, upload_to='gan_predict_img')),
                ('parent', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='recommendationEngine.GANPredictImage')),
                ('style_image', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='recommendationEngine.StyleImage')),
            ],
        ),
    ]
