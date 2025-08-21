from django.urls import path
from .import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',  views.dashboard_view, name='dashboard'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
