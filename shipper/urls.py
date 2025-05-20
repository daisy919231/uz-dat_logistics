from django.urls import path
from shipper.views import *
app_name='shipper'
urlpatterns = [
    path('api/freights/', freight_list_create, name='freight-list'),  # JSON API
    path('freights/', FreightTemplateView.as_view()),  # HTML Template
    #path('freight_detail/<int:id>/', FreightDetailAPIView.as_view(), name='freight-detail'),
    path('freight_update/<int:id>/', FreightUpdateAPIView.as_view(), name='freight-edit'),
    path('freight_delete/<int:id>/', FreightDelete.as_view(), name='freight-delete' ),
    path('freights/search/', FreightSearchView.as_view(), name='freight-search'),  # Public/Driver
    #path('all-freights/', AllFreights.as_view(), name='all-freights'),
]