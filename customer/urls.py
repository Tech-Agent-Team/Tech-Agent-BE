from django.urls import path

from .views import CustomerSignUpView
from accounts.views import CustomerOnlyView
urlpatterns=[
    path('signup/', CustomerSignUpView.as_view()),
    path('dashboard/', CustomerOnlyView.as_view(), name='customer-dashboard'),

]