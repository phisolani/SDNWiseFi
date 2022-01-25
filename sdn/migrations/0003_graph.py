# Generated by Django 3.0.6 on 2020-05-11 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sdn', '0002_tenant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iframe_url', models.CharField(max_length=200)),
                ('graph_type', models.CharField(choices=[('TH', 'Throughput'), ('DE', 'Queueing Delay')], max_length=2)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdn.Controller')),
            ],
        ),
    ]