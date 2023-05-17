from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views

from users import users_views, users_api_views
from rest_framework import routers

from users.users_views import CustomTokenObtainPairView

router = routers.SimpleRouter()
router.register(r'categories', users_api_views.CategoryCurd, basename="categories")
router.register(r'subcategories', users_api_views.SubCategoryCurd, basename="subcategories")
router.register(r'industries', users_api_views.IndustryCurd, basename="industries")
router.register(r'interestarea', users_api_views.InterestAreaCurd, basename="interestarea")
router.register(r'taxcurd', users_api_views.TaxCurd, basename="taxcurd")
router.register(r'solutions', users_api_views.SolutionCurd, basename="solution")
router.register(r'fetchOrders', users_api_views.FetchOrders, basename="fetchOrders")

# urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('vora.urls', namespace='vora')),
    path('summernote/', include('django_summernote.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/', users_views.change_password, name='change_password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Vora Dashboard"
admin.site.site_title = "Dashboard"
admin.site.index_title = "Dashboard"
