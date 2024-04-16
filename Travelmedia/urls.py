
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Travelmedia import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Travelmedia.accounts.urls')),
    path('', include('Travelmedia.hotels.urls')),
    path('', include('Travelmedia.common.urls')),

]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

