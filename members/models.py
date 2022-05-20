from django.db import models

# Create your models here.
class Order(models.Model):
    index = models.IntegerField(db_column='index')
    num_pedido = models.IntegerField(db_column='order_number', primary_key=True,verbose_name="pedido")  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    fecha = models.DateTimeField(db_column='order_date', blank=True, null=True,verbose_name="fecha")  # Field name made lowercase.
    cliente = models.TextField(db_column='order_user', blank=True, null=True,verbose_name="usuario")  # Field name made lowercase.
    email = models.TextField(db_column='order_email', blank=True, null=True)  # Field name made lowercase.
    estado = models.TextField(db_column='order_state', blank=True, null=True)  # Field name made lowercase.
    forma_de_pago = models.TextField(db_column='order_paymentmethod', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    promotion_id = models.TextField(db_column='order_promotion',blank=True, null=True)
    total = models.FloatField(db_column='order_total', blank=True, null=True)  # Field name made lowercase.
    total_pagado = models.FloatField(db_column='order_total_paid', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    order_items = models.TextField(db_column='order_items',blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'order'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

#comment

class OrderItem(models.Model):
    index = models.IntegerField(db_column='index',primary_key=True)
    producto = models.TextField(db_column='oi_producto', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nombre = models.TextField(db_column='oi_nombre', blank=True, null=True)  # Field name made lowercase.
    apellido_paterno = models.TextField(db_column='oi_apaterno', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    apellido_materno = models.TextField(db_column='oi_amaterno', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    correo = models.TextField(db_column='oi_email', blank=True, null=True)  # Field name made lowercase.
    rut = models.TextField(db_column='oi_rut', blank=True, null=True)  # Field name made lowercase.
    #num_pedido = models.IntegerField(db_column='Número de pedido', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    num_pedido = models.ForeignKey(Order,on_delete=models.DO_NOTHING,db_column='oi_order_number',related_name='num_pedidoOf')
    estado = models.TextField(db_column='oi_estado', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'order_item'

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_rut = models.CharField(max_length=15, blank=True, null=True)
    person_fechanac = models.DateField(blank=True, null=True)
    person_apaterno = models.CharField(max_length=30)
    person_amaterno = models.CharField(max_length=30, blank=True, null=True)
    person_nombres = models.CharField(max_length=30)
    person_email = models.CharField(max_length=50, blank=True, null=True)
    person_telefono = models.CharField(max_length=20, blank=True, null=True)
    person_apoderado_1 = models.IntegerField(db_column='person_apoderado1_id',blank=True, null=True)
    person_apoderado_2 = models.IntegerField(db_column='person_apoderado2_id',blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'person'