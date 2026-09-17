from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CakeViewSet

router = DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("cakes", CakeViewSet)

urlpatterns = router.urls