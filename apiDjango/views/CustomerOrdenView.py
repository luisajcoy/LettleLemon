from decimal import Decimal
from django.db import transaction
from django.utils import timezone # Obtiene fecha y hora
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Orden, OrdenItem, Cart
from ..serializers import OrdenSerializer
    
class CustomerOrdenCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrdenSerializer
    
    def get_queryset(self):
        return Orden.objects.filter(user= self.request.user)
    
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response({'error': 'Carrito vacío'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            total = sum((item.price for item in cart_items), Decimal('0.00'))
            
            orden = Orden.objects.create(
                user=request.user,
                delivery_crew=None,
                status=False,
                total=total,
                date=timezone.now().date()
            )
            
            orden_items = [
                OrdenItem(
                orden=orden,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
                )
                for item in cart_items
            ]
            OrdenItem.objects.bulk_create(orden_items)

            cart_items.delete()
            
        serializer = self.get_serializer(orden)
        return Response(serializer.data, status=status.HTTP_201_CREATED)