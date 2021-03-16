from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import StellarAccount, PublicProfile
from users.serializers import UserSerializer

class BalancesSerializer(serializers.Serializer):
    asset_code = serializers.CharField()
    issuer = serializers.CharField()
    balance = serializers.IntegerField()

class OperationsSerializer(serializers.Serializer):
    created_at = serializers.CharField()
    url = serializers.URLField()

class ClaimableBalancesSerializer(serializers.Serializer):
    id = serializers.CharField()
    sponsor = serializers.CharField()
    asset = serializers.CharField()
    amount = serializers.IntegerField()

class XDRSerializer(serializers.Serializer):
    xdr = serializers.CharField()

class StellarAccountSerializer(serializers.ModelSerializer):
    accountId = UserSerializer()

    class Meta:
        model = StellarAccount
        fields = ['accountId', 'public_key']
        lookup_field = 'user__username'

    def create(self, validated_data):
        try:
            account = StellarAccount.objects.get(accountId=request.user)
            raise APIException("You already have created a Stellar Account!")
        except StellarAccount.DoesNotExist:
            return StellarAccount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return ""       

class PublicProfileSerializer(serializers.ModelSerializer):
    accountId = UserSerializer()

    class Meta:
        model = PublicProfile   
        exclude = ('id', )
        lookup_field = 'user__username'

    def create(self, validated_data):
        user = self.context['request'].user
        print(user)
        raise APIException("nesho")
        try:
            account = StellarAccount.objects.get(accountId=request.user)
            raise APIException("You already have created a Stellar Account!")
        except StellarAccount.DoesNotExist:
            return StellarAccount.objects.create(**validated_data)


    def update(self, instance, validated_data):
        print(validated_data)

        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.description = validated_data.get('description', instance.description)
        instance.twitter_profile = validated_data.get('twitter_profile', instance.twitter_profile)
        instance.image_url = validated_data.get('image_url', instance.image_url)

        return instance

