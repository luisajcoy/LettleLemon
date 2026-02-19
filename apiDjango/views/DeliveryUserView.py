from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserSerializer
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404


class DeliveryUser(APIView):
    permission_classes = [IsAuthenticated]
    
    # Verificar si el usuario es manager 
    def is_manager(self, user):
        return user.groups.filter(name = 'Manage').exists()
    
    # Asignar rol a usuario
    def post(self, request):
        
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
              
        try:
            # Obtener usuario 
            user = User.objects.get(id=user_id)
            
            # Obtener Grupo 
            Delivery = Group.objects.get(name = 'Delivery Crew')
            
            # Asignar Rol 
            user.groups.add(Delivery)
            
            serializer = UserSerializer(user)
            return Response(
                {'message': f'Usuario {user.username} fue agregado exitosamente'},
                status=status.HTTP_201_CREATED
            )
            
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Listar los usuario delivery 
    def get(self, request):
        # Obtener el grupo
        group_delivery = Group.objects.get(name = 'Delivery Crew')
        
        # Obtener los usuarios de ese grupo
        usuarios = group_delivery.user_set.all()
        
        # Conversion de formato con serializer
        serializer = UserSerializer(usuarios, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DeliveryDelete(APIView):
    permission_classes = [IsAuthenticated]
        
    # Eliminar los usuarios del grupo 
    def delete(self, request, userId):
        # Verificar que el usuario exista 
        usuario = get_object_or_404(User, pk=userId)
            
        # Obtener el grupo 
        deliveryGroup= Group.objects.get(name = 'Delivery Crew')
            
        # Eliminar usuaria del grupo
        deliveryGroup.user_set.remove(usuario)
            
        serializer = UserSerializer(usuario)
        return Response(
            {
                'message': f'Usuario {usuario.username} eliminado exitosamente',
                'user': serializer.data
            },
            status=status.HTTP_200_OK
        )
        
            
            
        
        