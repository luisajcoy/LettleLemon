from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from ..serializers import UserSerializer
from django.shortcuts import get_object_or_404

class ManageUser(APIView):
    permission_classes = [IsAdminUser]
    
    # Listar los managers
    def get(self, request):
        # Obtener el grupo Manager
        managers_group = Group.objects.get(name = 'Manage')
        # Obtener todos los usuarios de ese grupo 
        usuarios = managers_group.user_set.all()
        # Conversion de formato con el serializer 
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    # Agregar un usuario al grupo
    def post(self, request):
        username = request.data.get('username')
        
        # Validacion 
        if not username:
            return Response(
                {'error', 'Username requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el usuario
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': f'Usuario {username} no existe'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Obtener grupo
        managers_group = Group.objects.get(name = 'Manage')
        
        # verificar si esta en el grupo 
        if managers_group.user_set.filter(id=usuario.id).exists():
            return Response(
                {'message': f'el usuario {username} ya es Manager'},
                status=status.HTTP_200_OK
            )
            
        # Agregar al grupo 
        managers_group.user_set.add(usuario)
        
        # Respuesta (usuario agregado)
        serializer = UserSerializer(usuario)
        return Response(
            {
                'message': f'{username} agregado a Manager',
                'usuario': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
class ManageDelete(APIView):
    
    permission_classes = [IsAdminUser]
        
    #Eliminar usuario del grupo 
    def delete(self, request,userId):
        #Verifica que usuario exista
        usuario = get_object_or_404(User, pk=userId)
        
        # Obtener el grupo manager
        try:
            manager_group =Group.objects.get(name = 'Manage')
        except Group.DoesNotExist:
            return Response(
                {'error': 'Grupo Manager no existe'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Verificar que el usuario este en el grupo
        if not manager_group.user_set.filter(id=usuario.id).exists():
            return Response(
                {'error': f'Usuario {usuario.username} no es Manager'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eliminar usuario del grupo 
        manager_group.user_set.remove(usuario)
        
        #Respuesta 
        return Response(
            {
                'message': f'Usuario {usuario.username} removino de Managers',
                'user_id': usuario.id,
                'username': usuario.username
            },
            status=status.HTTP_200_OK
        )