from django.urls import path

from .views import *

urlpatterns = [

    path('', UsersIndex.as_view(), name='home'),
    path('list', EmployeeList.as_view(), name="list_emp"),
    path('add', EmployeeAdd.as_view(), name="add_emp"),
    path('edit/<int:pk>', EmployeeUpdate.as_view(), name="edit_emp"),
    path('delete/<int:pk>', EmployeeDelete.as_view(), name="delete_emp"),
]