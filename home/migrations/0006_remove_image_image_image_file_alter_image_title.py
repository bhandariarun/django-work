# Generated by Django 4.2 on 2023-07-09 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.ImageField(null='True', upload_to='uploads/'),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
