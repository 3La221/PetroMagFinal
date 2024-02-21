from django.urls import path
from . import views

urlpatterns = [ 
    path('pointage/<int:ID>/',views.pointage,name='pointage'),
    path('',views.login_view,name='login'),
    path('add_chef_station/', views.add_chef_station, name='add_chef_station'),
    path('add_employe/<int:ID>/', views.add_employe, name='add_employe'),
    path('table_employe/<int:ID>/', views.table_employe, name='table_employe'),
    path('update_employe/<int:ID>/', views.update_employe, name='update_employe'),
    path('menu/<int:ID>/', views.menu_view, name='menu_view'),
    path('main/<int:ID>/', views.main_view, name='main_view'),
    path('employee_search/<int:ID>/', views.employee_search, name='employee_search'),
    path('affichage_mois/<int:ID>/', views.affichage_mois, name='affichage_mois'),
    path('pointage_mois/<int:ID>/', views.pointage_mois, name='pointage_mois'),
    
    path("logout/",views.logout_view,name="logout")
]