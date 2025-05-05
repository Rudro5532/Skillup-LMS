from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("Home_app.urls")),
    path("account/", include("Account_app.urls"))
]
