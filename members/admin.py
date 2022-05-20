from django.contrib import admin
from django.db import models
from members.models import OrderItem,Order,Person
from django.utils.safestring import mark_safe
from django.forms import TextInput, Textarea
import re

class CSSAdminMixin(object):
    class Media:
        css = {
            'all': ('css/fancy.css',)
        }

class OrderAdmin(admin.ModelAdmin,CSSAdminMixin):   
    formfield_overrides = {
        models.FloatField: {'widget': Textarea(attrs={'size':'8', 'style': 'text-align:right;border-top:none;border-left:none;border-right:none;border-radius:0;background:transparent;', }), },
        models.DateTimeField: {'widget': Textarea(attrs={'rows':1,'cols':10})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':80})},
        models.CharField: {'widget': Textarea(attrs={'rows':1, 'cols':80})},
        #models.TextField: {'widget': Textarea(attrs={'size':'4', 'style': 'text-align:right;border-top:none;border-left:none;border-right:none;border-radius:0;background:transparent;', }), },
    }
    
    search_fields = ['cliente','email']
    list_display = ['num_pedido','fecha','cliente','email','total','total_pagado','order','elementos_list']
    readonly_fields = ['cliente','fecha','elementos_list','image','externa']
    fields = ('cliente','fecha','elementos_list','image','externa')
 
    def order(self,obj):
            output = re.sub('\|','<br><br>',obj.order_items) #.replace('|',"<br><br><br>")
            return mark_safe(output)
    order.short_description = "Detalle"
    

    def image(self,obj):
            return mark_safe('<span style="color: green;"><img src="/static/img/logo.svg"/ height="20"> imagen</span>')
    def externa(self,obj):
            return mark_safe('<img src="https://www.cobsandcogs.cl/wp-content/themes/cobsandcogs/images/logo-white.svg"/>')
    def elementos_list(self,obj):
        elementos  = OrderItem.objects.filter(num_pedido=obj.num_pedido)
        if elementos.count() == 0:
            return '(None)'
        output = '<br><br> '.join([str(elemento.apellido_paterno)+' '+str(elemento.nombre)+' '+str(elemento.rut) for elemento in elementos])    
        return mark_safe(output)
    elementos_list.short_description = 'Miembros'
    elementos_list.allow_tags = True

class OrderItemAdmin(admin.ModelAdmin):
    #model = Forms
    #inlines=[OrdersInline]
    list_display = ['num_pedido','rut','get_detail']
    fields = ['num_pedido','rut']
    def get_detail(self,obj):
        return obj.num_pedido.total_pagado
    #list_filter = ['standard',] # ACA DEBO FILTRAR POR PRODUCTO año etc
    def __str__(self):
        return self.name

class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.FloatField: {'widget': Textarea(attrs={'size':'8', 'style': 'text-align:right;border-top:none;border-left:none;border-right:none;border-radius:0;background:transparent;', }), },
        models.DateTimeField: {'widget': Textarea(attrs={'rows':1,'cols':10})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':80})},
        models.CharField: {'widget': Textarea(attrs={'rows':1, 'cols':30})},
        #models.TextField: {'widget': Textarea(attrs={'size':'4', 'style': 'text-align:right;border-top:none;border-left:none;border-right:none;border-radius:0;background:transparent;', }), },
    }
    list_display = ['person_rut','person_apaterno','person_amaterno','person_nombres']
    search_fields = ['person_apaterno']
    fields = ['person_rut',('person_apaterno','person_amaterno','person_nombres')]
    

# Register your models here.
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Person,PersonAdmin)