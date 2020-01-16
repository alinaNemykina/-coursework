from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Order(models.Model):
    sum_total = models.IntegerField()
    client_id = models.ForeignKey('Client', models.DO_NOTHING)
    prod_id = models.ForeignKey('Product', models.DO_NOTHING)

    class Meta:
        db_table = 'order'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 60)
    gender = models.CharField(max_length = 20, blank = True, null = True)
    address = models.CharField(max_length = 60)
    bank_card_id = models.BigIntegerField(null = True)
    status = models.CharField(max_length = 50)
    phone_number = models.BigIntegerField(null = True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.client.save()

class Product(models.Model):
    color = models.CharField(max_length = 40)
    price = models.IntegerField()
    availability = models.BooleanField()
    pr_type = models.CharField(max_length = 50)
    size = models.IntegerField()
    disc = models.ManyToManyField('Discount', through = 'ProductDiscount')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.pr_type

class Discount(models.Model):
    percent = models.IntegerField()
    discount_type = models.CharField(max_length = 40)

    class Meta:
        db_table = 'discount'

    def __str__(self):
        return self.discount_type

class ProductDiscount(models.Model):
    prod_id = models.ForeignKey(Product, models.CASCADE)
    disc_id = models.ForeignKey(Discount, models.CASCADE)
    exp_date = models.DateField()

    class Meta:
        db_table = 'product_discount'