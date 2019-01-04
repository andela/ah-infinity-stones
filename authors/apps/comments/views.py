from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (CreateAPIView,
                                        RetrieveUpdateDestroyAPIView,
                                        RetrieveAPIView,
                                        UpdateAPIView,
                                        )
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# local imports
from .models import Comment
from .serializers import CommentSerializer
from .renderers import CommentJSONRenderer
from authors.apps.articles.models import User
from authors.apps.articles.models import Article
from authors.apps.core.paginator  import CommentPaginator
from authors.apps.core.permissions import IsAuthorOrReadOnly


class ArticleCommentAPIView(CreateAPIView):
    """A user can comment and view all comments on an article"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (CommentJSONRenderer,)
    pagination_class = CommentPaginator

    def post(self, request, slug=None):
        """Comment on an article"""
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # Build default data fields to override json
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, slug=None):
        """Get all comments on an article"""
        comment_set = Comment.objects.all()
        commentsBasket = []
        for comment in comment_set:
            serializer = CommentSerializer(comment)
            commentsBasket.append(serializer.data)
        commentsCount = len(commentsBasket)
        if commentsCount == 0:
            return Response({"Message":"There are no comments"}, status=status.HTTP_200_OK) 
        elif commentsCount == 1:
            return Response(commentsBasket, status=status.HTTP_200_OK) 
        else:
            commentsBasket.append({"commentsCount":commentsCount})
            rawPage = self.paginate_queryset(comment_set)
            if rawPage is not None:
                serializer = self.serializer_class(rawPage, many=True)
                return self.get_paginated_response(serializer.data)


class ArticleCommentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    """Views to edit a comment"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    renderer_classes = (CommentJSONRenderer,)

    def get_object(self):
        """Get one comments on an article"""
        comment_set = Comment.objects.all()
        if not comment_set:
            raise Http404
        for comment in comment_set:
            new_comment = get_object_or_404(Comment, pk=self.kwargs["id"])
            if comment.id == new_comment.id:
                self.check_object_permissions(self.request, comment)
                return comment

    def update(self, request, pk=None, **kwargs):
        """This function will update a comment"""
        self.permission_classes.append(IsAuthorOrReadOnly)
        comment = get_object_or_404(Comment, pk=self.kwargs["id"])
        self.check_object_permissions(self.request, comment)
        data = request.data
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"comment" : serializer.data, "Status": "Edited" }, status=status.HTTP_200_OK)

    def delete(self, request, slug=None, pk=None, **kwargs):
        """This function will delete a comment"""
        self.permission_classes.append(IsAuthorOrReadOnly)
        comment = get_object_or_404(Comment, pk=self.kwargs["id"])
        self.check_object_permissions(self.request, comment)
        serializer = self.serializer_class(comment)
        comment.delete()
        return Response({"Status": "Deleted" }, status=status.HTTP_200_OK)

