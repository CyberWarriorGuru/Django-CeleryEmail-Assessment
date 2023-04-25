from django.urls import path
from .views import LeadListCreateAPIView, LeadRetrieveUpdateDestroyAPIView, CampaignListCreateView, CampaignRetrieveUpdateDestroyView

urlpatterns = [
    path('leads/', LeadListCreateAPIView.as_view(), name='lead-list-create'),
    path('leads/<int:pk>/', LeadRetrieveUpdateDestroyAPIView.as_view(), name='lead-retrieve-update-destroy'),
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign_list_create'),
    path('campaigns/<int:pk>/', CampaignRetrieveUpdateDestroyView.as_view(), name='campaign_retrieve_update_destroy'),
]