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

from addendum import api as addendum
from medicalvitals import api as medicalvitals
from dentalvitals import api as dentalvitals
from visit import api as visit
from login import api as login
from consult import api as consult
from postreferral import api as postreferral
from medication import api as medication
from users import api as users
from order import api as order
from rest_framework_simplejwt import views as jwt_views
import patient.api as patient

from django.conf.urls.static import static
from django.conf import settings

print('lookee here ', settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.HelloView.as_view()),

    # JWT Token Endpoints
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    # Patient Creation/Retrieval Endpoints
    path('patients/new', patient.create_new, name='create_new'),
    path('patients/get', patient.get_details, name='get_details'),
    path('patients/update', patient.update_details, name='update_details'),
    path('patients/find_by_scan', patient.find_by_scan, name='find_by_scan'),
    path('patients/migrate', patient.migrate, name='migrate'),

    # Visit Creation/Retrieval Endpoints
    path('visit/new', visit.create_new, name='create_new'),
    path('visit/get', visit.get_details, name='get_details'),
    path('visit/update', visit.update_details, name='update_details'),
    path('visit/migrate', visit.migrate, name='migrate'),

    # Vitals Creation/Retrieval Endpoints
    path('medicalvitals/new', medicalvitals.create_new, name='create_new'),
    path('medicalvitals/get', medicalvitals.get_details, name='get_details'),
    path('medicalvitals/update', medicalvitals.update_details, name='update_details'),
    path('medicalvitals/migrate', medicalvitals.migrate, name='migrate'),

    # Visit Creation/Retrieval Endpoints
    path('dentalvitals/new', dentalvitals.create_new, name='create_new'),
    path('dentalvitals/get', dentalvitals.get_details, name='get_details'),
    path('dentalvitals/update', dentalvitals.update_details, name='update_details'),

    # Postreferral Creation/Retrieval Endpoints
    path('postreferrals/new', postreferral.create_new, name='create_new'),
    path('postreferrals/get', postreferral.get_details, name='get_details'),
    path('postreferrals/update', postreferral.update_details, name='update_details'),

    # Consult Creation/Retrieval Endpoints
    # path('consulttype/all', consult.get_all_consult_types, name='get_all_consult_types'),
    # path('consulttype/new', consult.create_new_consult_type, name='create_new_consult_type'),
    path('consults/new', consult.create_new, name='create_new'),
    path('consults/get', consult.get_details, name='get_details'),
    path('consults/migrate', consult.migrate, name='migrate'),

    # Medication
    path('medication/new', medication.create_new, name='create_new'),
    path('medication/get', medication.get_details, name='get_details'),
    path('medication/migrate', medication.migrate, name='migrate'),
    path('medication/update', medication.update_details, name='update_details'),
    path('medication/quantity', medication.update_quantity, name='update_quantity'),

    # User
    path('user/new', users.create_new, name='create_new'),
    path('user/get', users.get_details, name='get_details'),
    path('user/migrate', users.migrate, name='migrate'),

    # Addendum
    path('addendum/new', addendum.create_new, name='create_new'),

    # Order
    path('order/new', order.create_new, name='create_new'),
    path('order/get', order.get_details, name='get_details'),
    path('order/update', order.update_details, name='update_details'),
    path('order/migrate', order.migrate, name='migrate')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
