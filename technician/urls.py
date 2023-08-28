from django.urls import path

from .views import CustomerSignUpView
from accounts.views import TechnicianOnlyView
# from technician.views import techn
urlpatterns=[
    path('signup/', CustomerSignUpView.as_view()),
    path('dashboard/', TechnicianOnlyView.as_view(), name='Technician-dashboard'),

]