from django.db import models
from rest_framework.views import APIView


class MovieRating(models.TextChoices):
    RATED_G = "G"
    RATED_PG = "PG"
    RATED_PG13 = "PG-13"
    RATED_R = ("R",)
    RATED_NC17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20,
        choices=MovieRating.choices,
        default=MovieRating.RATED_G,
    )
    synopsis = models.TextField(null=True, default=None)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="movies",
    )

    orders = models.ManyToManyField(
        "users.User",
        through="movies.MovieOrder",
        related_name="orders_movies",
    )


class MovieOrder(models.Model):
    movie = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="movies_order",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_order",
    )

    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
