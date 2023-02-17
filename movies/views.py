from rest_framework.views import APIView, Request, Response, status
from .serializers import MovieSerializer, MovieOrderSerializer
from .models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsAdmOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, request: Request) -> Response:
        movie = Movie.objects.all().order_by("id")

        pages = self.paginate_queryset(movie, request)

        serializer = MovieSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrReadOnly]

    def get(self, request: Request, movies_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movies_id)
        seriealizer = MovieSerializer(movie)
        return Response(seriealizer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movies_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movies_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movies_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movies_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie_id=movies_id, user_id=request.user.id)
        return Response(serializer.data, status.HTTP_201_CREATED)
