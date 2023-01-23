from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('geography', views.geography, name='geography'),
    path('demand', views.demand, name='demand'),
    path('recent_vacancies', views.recent_vacancies, name='recent_vacancies'),
    path('skills', views.skills, name='skills'),
]