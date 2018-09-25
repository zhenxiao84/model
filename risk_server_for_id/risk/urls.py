from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.risk),
    url(r'^gzip', views.risk_for_gzip),
]
