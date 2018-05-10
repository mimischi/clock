from django.urls import include, path
from rest_framework import routers

from clock.contracts.api import views

router = routers.DefaultRouter()
router.register(
    'contracts', views.ContractEndDateViewSet, base_name='end_date'
)

urlpatterns = [path('', include(router.urls))]
