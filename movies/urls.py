from django.urls import path
from .views import MovieView, MovieDetailView, OrderView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movies_id>/", MovieDetailView.as_view()),
    path("movies/<int:movies_id>/orders/", OrderView.as_view()),
]
