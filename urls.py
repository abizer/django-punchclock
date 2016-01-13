
"""
punchclock app URL Configuration
"""

from django.conf.urls import url
from punchclock import views

app_name = 'punchclock'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^clock_in', views.clock_in, name = 'clock_in'),
    url(r'^clock_out', views.clock_out, name = 'clock_out'),

    # login support for standalone usage
    url(r'^login', views.employee_login, name = 'login'),
    url(r'^logout', views.employee_logout, name = 'logout'),
]
