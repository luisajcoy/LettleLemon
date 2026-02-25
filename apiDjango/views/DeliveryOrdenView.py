from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from ..models import Orden 
from ..serializers import OrdenSerializer

# ListaApi - Solo lectura
class DeliveryOrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrdenSerializer
    
    def get_query(self):
        # Filtra las ordenes asignadas al repartidor autenticado actualmente 
        return Orden.objects.filter(Delivery_Crew = self.request.user)
    