from rest_framework import serializers

class BalancesSerializer(seerializers.Serializer):
    asset_code = serializers.CharField()
    issuer = serializers.CharField()
    balance = serializers.IntegerField()
