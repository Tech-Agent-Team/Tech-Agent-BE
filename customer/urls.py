from django.urls import path

from .views import Customerordersfeed, CustomerSignUpView ,Customermyorders , Customerdeletorders , Customerordersdone
from accounts.views import CustomerOnlyView
urlpatterns=[
    path('signup/', CustomerSignUpView.as_view()),
    path('dashboard/', CustomerOnlyView.as_view(), name='customer-dashboard'),
    path('myorders/', Customermyorders.as_view(), name='customer-myorders'),
    path('deletorders/<int:order_id>/', Customerdeletorders.as_view(), name='customer-myorders'),
    path('ordersdone/<int:order_id>/', Customerordersdone.as_view(), name='customer-myorders'),
    path('feedback/<int:order_id>/', Customerordersfeed.as_view(), name='customer-myorders'),


]