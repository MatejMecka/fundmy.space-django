from django.shortcuts import render
from rest_framework import views
from .utils import getAssets
from .serializers import BalancesSerializer

# Create your views here.

class Balances(views.APIView):
    def get(self, request):
        data = getAssets()
        results = BalancesSerializer(data,many=True).data 
        return Response(results)
