from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAdminUser
from ..serializers import CategorySerializer

class CategoryAdd(APIView):
    permission_classes = [IsAdminUser]
    
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
        
        
        
    
