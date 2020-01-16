from django.core.management.base import BaseCommand, CommandError
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from lxml import etree, objectify
from django.contrib.auth.models import User
from store.models import *
from django.core import serializers

def create_client_appt(data):
    """
    Создаем структуру XML(Client).
    """
    appt = objectify.Element("Client")
    appt.id = data["id"]
    appt.full_name = data["full_name"]
    appt.gender = data["gender"]
    appt.address = data["address"]
    appt.bank_card_id = data["bank_card_id"]
    appt.status = data["status"]
    appt.phone_number = data["phone_number"]
    appt.user_id = data["user_id"]
    return appt

def create_ord_appt(data):
    """
    Создаем структуру XML(Order).
    """
    appt = objectify.Element("Order")
    appt.id = data["id"]
    appt.sum_total = data["sum_total"]
    appt.client_id_id = data["client_id_id"]
    appt.prod_id_id = data["prod_id_id"]
    return appt

def create_prod_appt(data):
    """
    Создаем структуру XML(Product).
    """
    appt = objectify.Element("Product")
    appt.id = data["id"]
    appt.color = data["color"]
    appt.price = data["price"]
    appt.availability = data["availability"]
    appt.pr_type = data["pr_type"]
    appt.size = data["size"]
    appt.disc = data["disc"]
    return appt

def create_prod_disc_appt(data):
    """
    Создаем структуру XML(ProductDiscount).
    """
    appt = objectify.Element("ProductDiscount")
    appt.id = data["id"]
    appt.prod_id = data["prod_id"]
    appt.disc_id = data["disc_id"]
    appt.exp_date = data["exp_date"]
    return appt

def create_disc_appt(data):
    """
    Создаем структуру XML(Discount).
    """
    appt = objectify.Element("Discount")
    appt.id = data["id"]
    appt.percent = data["percent"]
    appt.discount_type = data["discount_type"]
    return appt

def create_user_appt(data):
    """
    Создаем структуру XML(User).
    """
    appt = objectify.Element("User")
    appt.id = data["id"]
    appt.password = data["password"]
    appt.last_login = data["last_login"]
    appt.is_superuser = data["is_superuser"]
    appt.username = data["username"]
    appt.email = data["email"]
    appt.is_staff = data["is_staff"]
    appt.is_active = data["is_active"]
    appt.date_joined = data["date_joined"]
    return appt

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        xml = '<Store>'+'</Store>'

        root = objectify.fromstring(xml)

        clients = Client.objects.all()

        for client in clients:

            appt = create_client_appt({"id":client.id,
                                       "full_name":client.full_name,
                                       "gender":client.gender,
                                       "address":client.address,
                                       "bank_card_id":client.bank_card_id,
                                       "status":client.status,
                                       "phone_number":client.phone_number,
                                       "user_id":client.user.id}
                                       )
    
            root.append(appt)

        orders = Order.objects.all()

        for order in orders:

            appt = create_ord_appt({"id":order.id,
                                    "sum_total":order.sum_total,
                                    "client_id_id":order.client_id_id,
                                    "prod_id_id":order.prod_id_id}
                                    )
    
            root.append(appt)

        products = Product.objects.all()

        for product in products:

            appt = create_prod_appt({"id":product.id,
                                     "color":product.color,
                                     "price":product.price,
                                     "availability":product.availability,
                                     "pr_type":product.pr_type,
                                     "size":product.size,
                                     "disc":product.disc}
                                     )
    
            root.append(appt)
        
        discounts = Discount.objects.all()

        for discount in discounts:

            appt = create_disc_appt({"id":discount.id,
                                     "percent":discount.percent,
                                     "discount_type":discount.discount_type}
                                     )
    
            root.append(appt)

        prods_discs = ProductDiscount.objects.all()

        for prod_disc in prods_discs:

            appt = create_prod_disc_appt({"id":prod_disc.id,
                                          "prod_id":prod_disc.prod_id,
                                          "disc_id":prod_disc.disc_id,
                                          "exp_date":prod_disc.exp_date,}
                                     )
    
            root.append(appt)

        users = User.objects.all()

        for user in users:

            appt = create_user_appt({"id":user.id,
                                     "password":user.password,
                                     "last_login":user.last_login,
                                     "is_superuser":user.is_superuser,
                                     "username":user.username,
                                     "email":user.email,
                                     "is_staff":user.is_staff,
                                     "is_active":user.is_active,
                                     "date_joined":user.date_joined}
                                     )
    
            root.append(appt)

        # удаляем все lxml аннотации.
        objectify.deannotate(root)
        etree.cleanup_namespaces(root)
        
        # конвертируем все в xml структуру.
        obj_xml = etree.tostring(root,
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True)        

        try:
            with open("store.xml", "wb") as xml_writer:
                xml_writer.write(obj_xml)
        except IOError:
            pass