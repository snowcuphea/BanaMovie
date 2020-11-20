from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('is-admin/', views.is_admin),
    path('manage_members/', views.manage_members),

]