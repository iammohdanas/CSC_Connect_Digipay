"""csc_connect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboarddigipay, name='dashboarddigipay'),
    path('redirect_fun/', views.redirect_fun, name='redirect_fun'),
    path('digipay-npci-connect-login/', views.process_login, name='process_login'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    path('transactionform/',views.transactionform,name='transactionform'),
    path('process_withdrawform/', views.process_withdrawform, name='process_withdrawform'),
    path('authdevregister/',views.authdevregister,name='authdevregister'),
    path('aepslogs/',views.aepslogs,name='aepslogs'),
    path('walletTopup/',views.walletTopup,name='walletTopup'),
    path('walletTopupProcess/',views.wallet_topup_process,name='walletTopupProcess'),
    path('passbook/',views.passbook,name='passbook'),
    path('dashboard/',views.dashboarddigipay,name='dashboarddigipay'),
    path('base2/',views.base2,name='base2'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('afterloginbioauth',views.afterloginbioauth,name='afterloginbioauth')
]