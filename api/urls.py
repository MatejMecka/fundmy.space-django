from django.urls import include, path
from .views import Balances, StellarAccountView, PublicProfilesView, Operations, ClaimableBalances
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stellarAccount', StellarAccountView, basename='stellarAccount')
router.register(r'publicProfile', PublicProfilesView, basename='publicProfile')
urlpatterns = router.urls

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('users/', include('users.urls')),
    path('balances/', Balances, name='balances'),
    path('operations/', Operations, name='operations'),
    path('claimable-balances/', ClaimableBalances, name='claimable-balances'),
]

urlpatterns += router.urls
