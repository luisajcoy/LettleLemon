from django.urls import path
from .views import ManageUser, ManageDelete, CategoryAdd, DeliveryUser, DeliveryDelete, MenuItemAdd, DeliveryOrderListView, DeliveryOrderUpdateView, MenuItemListView, MenuItemByCategory 

urlpatterns = [
    # GRUPOS
    path('group/manager/users', ManageUser.as_view(), name='manage-users'),
    path('group/manager/users/<int:userId>', ManageDelete.as_view(), name='manage-delete'),
    
    # CATEGORIA
    path('category/add', CategoryAdd.as_view(), name='category-add'),
    
    # DELIVERY
    path('group/delivery/users', DeliveryUser.as_view(), name= 'delivery-users'),
    path('group/delivery/users/<int:userId>', DeliveryDelete.as_view(), name='delivery-delete'),
    path('delivery/orders', DeliveryOrderListView.as_view(), name= 'delivery-orders'),
    path('delivery/orders/<int:pk>/status', DeliveryOrderUpdateView.as_view(), name= 'delivery-order-update-status'),
    
    # MENUITEMS
    path('menu/item/add', MenuItemAdd.as_view(), name='menuitem-add'),
    path('menu/item/all', MenuItemListView.as_view(), name='menuitem-all'),
    path('menu/item/category/<int:category_id>', MenuItemByCategory.as_view(), name='menuitem-by-category')
]

