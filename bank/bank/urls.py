"""bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bankapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login', views.login),
    path('newuser', views.newuser),
    path('edituser', views.edituser),
    path('blockuser', views.blockuser),
    path('trans', views.trans),
    path('passwd', views.passwd),
    path('user_created', views.user_created),
    path('search', views.search),
    path('locate', views.locate),
    path('update_success', views.update_success),
    path('update_passwd', views.update_passwd),
    path('block_success', views.block_success),
    path('admin_portal', views.admin_portal),
    path('home_portal', views.home),
    path('custForm', views.custForm),
    path('custlog', views.custlog),
    path('update_cust_passwd', views.update_cust_passwd),
    path('update_trans', views.update_trans),
    path('transsearch', views.transsearch),
    path('locatetrans', views.locatetrans),
    path('revtrans', views.revtrans),
]
