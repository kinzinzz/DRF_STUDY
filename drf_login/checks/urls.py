from django.urls import path
from . import views

app_name = 'checks'

urlpatterns = [
    path('', views.check_list),
    path('create/', views.create_check),
    path('<int:check_pk>', views.check_detail),
]