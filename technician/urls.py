from django.urls import path
from .views import TechnicianSignUpView,homeTechnicianView,TechnicianAcceptedOrdersView,TechnicianCancelOrdersView,TechnicianProfileView
# from .views import TechnicianUpdateProfileView
urlpatterns=[
    path('signup/', TechnicianSignUpView.as_view()),
    path('profile/<str:user_name>/', TechnicianProfileView.as_view(), name='Technician-dashboard'),
    # path('profileupdate/', TechnicianUpdateProfileView.as_view()),    
    path('hometechnician/', homeTechnicianView.as_view(), name='Technician-home'),
    path('techacceptedlist/', TechnicianAcceptedOrdersView.as_view(), name='Technician-accepted'),
    path('cancelorder/<int:order_id>/', TechnicianCancelOrdersView.as_view(), name='Technician-cancel'),

]