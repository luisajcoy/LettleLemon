from django.urls import path
from .views import ManageUser, ManageDelete

urlpatterns = [
    path('group/manager/users', ManageUser.as_view(), name='manage-users'),
    path('group/manager/users/<int:userId>', ManageDelete.as_view(), name='manage-delete'),
]

