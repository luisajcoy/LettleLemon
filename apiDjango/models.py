from django.db import models
# Importacion de usuarios 
from django.contrib.auth.models import User


# Creacion de Modelos
class Category(models.Model):
    slug = models.SlugField()
    # El db_index es cuando un campo se usara para muchas busquedas
    title = models.CharField(max_length=255, db_index=True)
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        # Registros unicos - Un usuario no puede tener el mismo producto dos veces en su carrito
        unique_together = ('menuitem','user')
        
class Orden(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # El SET_NULL -> si se elimina el usuario no se elimina la orden
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)
    
class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models. SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        # Asegura que en la misma orden no se puede agregar el mismo producto dos veces
        unique_together = ('orden','menuitem')
    
