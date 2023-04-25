from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import JsonResponse
from .models import Lead, Campaign, ConnectedEmail
from .serializers import LeadSerializer, CampaignSerializer



class LeadListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


class LeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

