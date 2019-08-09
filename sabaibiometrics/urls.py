"""sabaibiometrics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from visit import api as visit
from login import api as login
from rest_framework_simplejwt import views as jwt_views
import patient.api as patient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.HelloView.as_view()),

    # JWT Token Endpoints
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Patient Creation/Retrieval Endpoints
    path('patients/all', patient.get_all_patients, name='get_all_patients'),
    path('patients/by_name', patient.get_patient_by_name, name='get_patient_by_name'),
    path('patients/by_id', patient.get_patient_by_id, name='get_patient_by_id'),
    path('patients/new', patient.create_new_patient, name='new_patient'),
    path('patients/image_by_id', patient.get_patient_image_by_id, name='patient_image'),
    path('patients/update_by_id', patient.update_patient, name='patient_update'),

    # Patient Visit Creation/Retrieval Endpoints
    path('visit/new', visit.create_new_visit, name='create_visit'),
    path('visit/by_id', visit.get_visit_by_id, name='get_visit_by_id'),
    path('visit/by_patient', visit.get_visit_by_patient, name='get_visit_by_patient'),
    path('visit/by_status', visit.get_visit_by_status, name='get_visit_by_status')
]
