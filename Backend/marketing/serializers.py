from rest_framework import serializers
from .models import Campaign, CampaignChannel

class CampaignChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignChannel
        fields = ['id', 'channel_type', 'is_active', 'config_json']

class CampaignSerializer(serializers.ModelSerializer):
    channels = CampaignChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'status', 'created_at', 'channels']
        read_only_fields = ['status', 'created_at', 'channels']
