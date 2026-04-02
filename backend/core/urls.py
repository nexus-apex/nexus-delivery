from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deliveryorders/', views.deliveryorder_list, name='deliveryorder_list'),
    path('deliveryorders/create/', views.deliveryorder_create, name='deliveryorder_create'),
    path('deliveryorders/<int:pk>/edit/', views.deliveryorder_edit, name='deliveryorder_edit'),
    path('deliveryorders/<int:pk>/delete/', views.deliveryorder_delete, name='deliveryorder_delete'),
    path('deliverydrivers/', views.deliverydriver_list, name='deliverydriver_list'),
    path('deliverydrivers/create/', views.deliverydriver_create, name='deliverydriver_create'),
    path('deliverydrivers/<int:pk>/edit/', views.deliverydriver_edit, name='deliverydriver_edit'),
    path('deliverydrivers/<int:pk>/delete/', views.deliverydriver_delete, name='deliverydriver_delete'),
    path('deliveryroutes/', views.deliveryroute_list, name='deliveryroute_list'),
    path('deliveryroutes/create/', views.deliveryroute_create, name='deliveryroute_create'),
    path('deliveryroutes/<int:pk>/edit/', views.deliveryroute_edit, name='deliveryroute_edit'),
    path('deliveryroutes/<int:pk>/delete/', views.deliveryroute_delete, name='deliveryroute_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
