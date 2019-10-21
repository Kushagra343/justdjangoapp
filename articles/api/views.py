# from rest_framework import viewsets

# class ArticleViewSet(viewsets.ModelViewSet):
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all()
from django.http import JsonResponse
from django.http import Http404

from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from articles.models import Article
from .serializers import ArticleSerializer
from rest_framework.authtoken.models import Token


class ArticleListView(ListAPIView):
    queryset = Article.objects.filter(job_status='CREATED')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )


class ArticleDetailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)

        owner = article.employer.username
        job_status = article.job_status
        token = request.headers.get('Authorization')

        user_obj = Token.objects.get(key=token).user

        display_text = ""
        if job_status == 'CREATED':
            if owner == user_obj.username:
                display_text = "Job Created"
            else:
                display_text = "Accept Job"
        elif job_status == 'ACCEPTED':
            if user_obj.username == str(article.employee):
                display_text = "Complete Job"
            else:
                display_text = "Job Has Been Accepted"
                display_text = "Complete Job"
        elif job_status == 'COMPLETED':
            display_text = "Job Has Been Completed"

        serializer = ArticleSerializer(article)
        context = {}
        context.update(serializer.data)
        context.update(
            {"display_text": display_text})
        return Response(context)


class ArticleCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            Article.objects.create(
                title=request.data["title"], content=request.data["content"], budget=request.data["budget"], employer=request.user)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False)


class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ArticleJobStatusUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        job_status = article.job_status
        user_obj = request.user

        if job_status == 'CREATED':
            if not article.employee:
                article.employee = request.user
            article.job_status = 'ACCEPTED'
            article.save()
        elif job_status == 'ACCEPTED':
            if user_obj.username == article.employee.username:
                article.job_status = 'COMPLETED'
                article.save()

        serializer = ArticleSerializer(article)
        return Response(serializer.data)
