from django.urls import path
from .views import *


urlpatterns = [
    path('', DorixonaList.as_view()),
    path('<int:pk>/', DorixonaDetail.as_view()),
    path('dorilar/', dori_list),
    path('viloyatlar/', ViloyatList.as_view()),
    path('tumanlar/', TumanList.as_view()),
]