from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from ..models import Orden 
from ..serializers import OrdenStatusSerializer

class DeliveryOrderUpdateView(UpdateAPIView):
    serializer_class = OrdenStatusSerializer
    permission_classes = [IsAuthenticated]
    # Buscara la orden por el ID 
    lookup_field = 'pk'
    
    # Filtra las ordenes por id del usuario
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name = 'Delivery crew').exists():
            # Retorna solo las ordenes asignadas a ese delivery 
            return Orden.objects.filter(delivery_crew = user)
        
        # Si no es delivery no retornar nada
        return Orden.objects.none()
    
    # Actualiza el status 
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial= True)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    'message' : 'Estado actualizado',
                    'orden_id' : instance.id,
                    'status': serializer.data['status']
                }, status= status.HTTP_200_OK
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)