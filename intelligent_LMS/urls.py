from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("Home_app.urls")),
    path("account/", include("Account_app.urls")),
    path("course/", include("Courses_app.urls")),
    path("payment/",include("Payment_app.urls")),
    path("", include("Core_app.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
