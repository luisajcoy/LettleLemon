from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..serializers import CategorySerializer
from ..models import Category

class CategoryAdd(APIView):
    
    # Permisos segun el metodo
    def get_permissions(self):
        if self.request.method== 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    # Agregar o crear una categoria 
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        
        # Validacion con serializer 
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': f'Categoria {serializer.data["title"]} creada exitosamente',
                    'categoria': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
            
        # Respuesta con errores de validacion
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # Ver o listar todas las categorias
    def get(self, request):
        categoria = Category.objects.all()
        serializador = CategorySerializer(categoria, many=True)
        return Response(
            {
            'categorias': serializador.data
            }, status=status.HTTP_200_OK
        )       
        
        
    
