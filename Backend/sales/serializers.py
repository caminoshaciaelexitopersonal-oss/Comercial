from rest_framework import serializers
from .models import Opportunity, StageHistory

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['id', 'name', 'stage', 'value', 'created_at', 'updated_at', 'owner']

class StageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StageHistory
        fields = '__all__'
