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
    """A user can comment on an article"""
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = (CommentJSONRenderer,)

    def post(self, request, art_slug=None):
        """Comment on an article"""
        article = get_object_or_404(Article, art_slug=self.kwargs["art_slug"]) 
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, art_slug=None):
        """Get all the comments on an article"""
        article = get_object_or_404(Article, art_slug=self.kwargs["art_slug"])
        comment_set = Comment.objects.filter(article__id=article.id)
        comments = []
        for comment in comment_set:
            serializer = CommentSerializer(comment)
            comments.append(serializer.data)
        commentsCount = len(comments)
        comments.append({"commentsCount":commentsCount})
        return Response(comments, status=status.HTTP_200_OK) 
        if commentsCount == 0:
            return Response({"Message":"There are no comments for this article"}, status=status.HTTP_200_OK) 
        elif commentsCount == 1:
            return Response(comments, status=status.HTTP_200_OK) 
        else:
            comments.append({"commentsCount":commentsCount})
            page = self.paginate_queryset(comment_set)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)


class ArticleCommentUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    """Views to edit a comment"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    renderer_classes = (CommentJSONRenderer,)

    def get_object(self):
        """Get one comment on an article"""
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

    def delete(self, request, art_slug=None, pk=None, **kwargs):
        """This function will delete a comment"""
        self.permission_classes.append(IsAuthorOrReadOnly)
        comment = get_object_or_404(Comment, pk=self.kwargs["id"])
        self.check_object_permissions(self.request, comment)
        serializer = self.serializer_class(comment)
        comment.delete()
        return Response({"Status": "Deleted" }, status=status.HTTP_200_OK)

