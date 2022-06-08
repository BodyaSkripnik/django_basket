from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('homepage/', homepage, name='homepage'),
    path('logout/', logout_user, name='logout'),
    path('category/<slug:category_slug>',get_categorys,name='category'),
    path('basket/,<int:id_prod>',basket,name='basket'),
    path('show_basket/',show_basket,name='show_basket'),
    path('delete_basket/',delete_basket,name='delete_basket'),
    path('udateplus/',udateplus,name='udateplus'),
    path('udateminus/',udateminus,name='udateminus'),



]

