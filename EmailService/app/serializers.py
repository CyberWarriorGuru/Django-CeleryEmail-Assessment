from rest_framework import serializers
from .models import Lead, Campaign


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'company', 'website']
        
class CampaignSerializer(serializers.ModelSerializer):
    leads = LeadSerializer(many=True)

    class Meta:
        model = Campaign
        fields = '__all__'