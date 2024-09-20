from rest_framework.routers import DefaultRouter 
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register("save-pay", views.CourseGenericViewset)
router.register("webhook", views.WebHookViewSet)

urlpatterns = [
    path("",include(router.urls)),
    path("init-pay", views.InitiatePayment.as_view()),
    path("check-pay", views.CheckPayment.as_view()),
    path("redeem-pay", views.RedeemPayment.as_view()),
    # path("webhook", views.WebHookViewSet.as_view()),
    # path("save-pay", views.InitiatePayment.as_view())
]
