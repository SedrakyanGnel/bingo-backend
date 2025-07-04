from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import MeViewSet, RegisterView
from bins.views  import BinViewSet
from scans.views import ScanEventViewSet
from rewards.views import RewardViewSet, RedemptionViewSet
from points.views import BalanceViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register("me",          MeViewSet, basename="me")
router.register("bins",        BinViewSet)
router.register("scans",       ScanEventViewSet, basename="scans")
router.register("rewards",     RewardViewSet)
router.register("redemptions", RedemptionViewSet, basename="redemptions")
router.register("balance",     BalanceViewSet, basename="balance")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/token/",    TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)