from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from ..serializers import CartSerializer
from ..models import Cart

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Ver todos los items del carrito del usuario autenticado
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Agregar item al carrito
    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Eliminar todos los items del carrito del usuario
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Carrito vaciado"}, status=status.HTTP_200_OK)