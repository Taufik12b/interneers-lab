from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

def hello_world(request):
    name = request.GET.get("name", "world")  # Get 'name' from query params, default to 'world'
    # return HttpResponse(f"Hello, {name}! This is our interneers-lab Django server.")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('', include(router.urls)),
]
