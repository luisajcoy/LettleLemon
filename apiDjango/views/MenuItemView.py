from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User,Group
from ..serializers import MenuItemSerializer
from ..models import MenuItem, Category

class MenuItemAdd(APIView):
    permission_classes = [IsAuthenticated]
    
    # Agregar MenuItem a una categoria 
    def post(self, request):
        
        try:
            # Extraer datos
            category_id = request.data.get('category_id')
            title = request.data.get('title')
            price = request.data.get('price')
            featured = request.data.get('featured')
            
            # Buscar categoría
            category = Category.objects.get(id=category_id)
            
            # Crear MenuItem directamente
            menu_item = MenuItem.objects.create(
                title=title,
                price=price,
                featured=featured,
                category=category
            )
            serializer = MenuItemSerializer(menu_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Category.DoesNotExist:
            return Response({"error": "Categoría no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    