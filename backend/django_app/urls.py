from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.http import JsonResponse


def hello_world(request):
    name = request.GET.get("name", "world")  # Get 'name' from query params, default to 'world'
    # return HttpResponse(f"Hello, {name}! This is our interneers-lab Django server.")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
]