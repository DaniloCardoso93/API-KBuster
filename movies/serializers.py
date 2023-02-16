from rest_framework import serializers
from .models import MovieRating, Movie, MovieOrder


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default=None)
    rating = serializers.ChoiceField(
        choices=MovieRating.choices,
        default=MovieRating.RATED_G,
    )
    synopsis = serializers.CharField(default=None)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField()
    price = serializers.DecimalField(decimal_places=2, max_digits=8)
    buyed_by = serializers.SerializerMethodField()
    buyed_at = serializers.DateTimeField(read_only=True)

    def get_title(self, obj):
        return obj.movie.title

    def get_buyed_by(self, obj):
        return obj.user.email

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
