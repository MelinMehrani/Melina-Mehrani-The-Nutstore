# Generated by Django 4.2.2 on 2023-06-28 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=500)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nutstore.city')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('pistachio', 'Pistachio'), ('almond', 'Almond'), ('cashew', 'Cashew'), ('peanuts', 'Peanuts'), ('confectioneries', 'Confectioneries'), ('dried fruits', 'Dried Fruits'), ('snacks', 'Snacks'), ('other', 'Other Products')], max_length=200)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nutstore.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('preparing', 'Preparing'), ('delivered', 'Delivered')], default='preparing', max_length=20)),
                ('items', models.ManyToManyField(to='Nutstore.cartitem')),
            ],
        ),
    ]