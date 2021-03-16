from django.shortcuts import render
from rest_framework import views, status
from rest_framework.decorators import api_view
from .utils import getAssets, getClaimableBalances, getOperations
from .serializers import BalancesSerializer, StellarAccountSerializer, PublicProfileSerializer, OperationsSerializer, ClaimableBalancesSerializer
from .models import StellarAccount, PublicProfile
from rest_framework.parsers import JSONParser
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def Balances(request):
    try:
        public_key = StellarAccount.objects.get(accountId=request.user).public_key
        data = getAssets(public_key)
        results = BalancesSerializer(data, many=True)
        print(results)
        return Response(results.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def ClaimableBalances(request):
    try:
        public_key = StellarAccount.objects.get(accountId=request.user).public_key
        data = getClaimableBalances(public_key)
        print(data)
        results = ClaimableBalancesSerializer(data, many=True)
        print(results)
        return Response(results.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Operations(request):
    try:
        public_key = StellarAccount.objects.get(accountId=request.user).public_key
        data = getOperations(public_key)
        print(data)
        results = OperationsSerializer(data, many=True)
        return Response(results.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def SubmitXDR(request):
    try:
        public_key = StellarAccount.objects.get(accountId=request.user).public_key
        data = request.data
        
        

        return Response(results.data)



    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)
        


class StellarAccountView(viewsets.ModelViewSet):
    queryset = StellarAccount.objects.all().select_related('accountId')
    serializer_class = StellarAccountSerializer
    lookup_field = 'accountId__username'

class PublicProfilesView(viewsets.ModelViewSet):
    queryset = PublicProfile.objects.all().select_related('accountId')
    serializer_class = PublicProfileSerializer
    lookup_field = 'accountId__username'