from django.urls import path
from .views import ManageUser, ManageDelete, CategoryAdd, DeliveryUser, DeliveryDelete

urlpatterns = [
    # GRUPOS
    path('group/manager/users', ManageUser.as_view(), name='manage-users'),
    path('group/manager/users/<int:userId>', ManageDelete.as_view(), name='manage-delete'),
    
    # CATEGORIA
    path('category/add', CategoryAdd.as_view(), name='category-add'),
    
    # DELIVERY
    path('group/delivery/users', DeliveryUser.as_view(), name= 'delivery-users'),
    path('group/delivery/users/<int:userId>', DeliveryDelete.as_view(), name='delivery-delete'),
]

