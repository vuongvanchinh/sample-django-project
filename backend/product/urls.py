from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('category',views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('variants', views.ProductVariantViewSet)
urlpatterns = router.urls

