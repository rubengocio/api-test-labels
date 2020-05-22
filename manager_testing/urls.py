"""reclamos_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from manager_testing.views.access_point import AccessPointListView, AccessPointNewView, AccessPointEditView
from manager_testing.views.carriers import CarriersListView, CarrierNewView, CarrierEditView
from manager_testing.views.index import index
from manager_testing.views.prueba import TestListView, TestRunView, TestNewView, TestEditView
from manager_testing.views.resultado import TestPlanFailResultListView, \
    TestPlanSuccessResultListView, TestPlanDetailResultListView, TestPlanReloadResultView
from manager_testing.views.services import ServiceListView, ServiceNewView, ServiceEditView
from manager_testing.views.test_plan import TestPlanDetailView, TestPlanListView

urlpatterns = [
    path('', index, name='index'),
    path('form-test-plan/<int:pk>', TestPlanDetailView.as_view(), name="form-test-plan"),
    path('test-plans', TestPlanListView.as_view(), name="test-plans"),
    path('tests', TestListView.as_view(), name="tests"),
    path('test', TestNewView.as_view(), name="new-test"),
    path('test/<int:pk>', TestEditView.as_view(), name="edit-test"),
    path('run_test/<int:pk>', TestRunView.as_view(), name="run_test"),
    path('success_results/<int:pk>', TestPlanSuccessResultListView.as_view(), name="success_results"),
    path('fail_results/<int:pk>', TestPlanFailResultListView.as_view(), name="fail_results"),
    path('detail_results/<int:pk>', TestPlanDetailResultListView.as_view(), name="detail_results"),
    path('reload_result/<int:pk>', TestPlanReloadResultView.as_view(), name="reload_result"),
    path('access_points', AccessPointListView.as_view(), name="access_points"),
    path('access_point', AccessPointNewView.as_view(), name="new-access_points"),
    path('access_point/<int:pk>', AccessPointEditView.as_view(), name="edit-access_points"),
    path('carriers', CarriersListView.as_view(), name="carriers"),
    path('carrier', CarrierNewView.as_view(), name="new-carrier"),
    path('carrier/<int:pk>', CarrierEditView.as_view(), name="edit-carrier"),
    path('services', ServiceListView.as_view(), name="services"),
    path('service', ServiceNewView.as_view(), name="new-service"),
    path('service/<int:pk>', ServiceEditView.as_view(), name="edit-service"),
]