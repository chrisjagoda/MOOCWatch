from allauth.account.views import ConfirmEmailView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status,viewsets
from rest_framework.response import Response
from app.serializers import *
from app.permissions import *
from app.api import *

class ConfirmEmailView(ConfirmEmailView):
    template_name = 'app/email_verification.html'

# REST API Endpoints

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ReadOnly)

class CourseTakerViewSet(viewsets.ModelViewSet):
    serializer_class = CourseTakerSerializer
    
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        """
        This view should return a list of all the courses
        for the currently authenticated user.
        """
        user = self.request.user
        return CourseTaker.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        try:
            print(self.request.user)
            obj = CourseTakerSerializer.objects.create()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response = super(CourseTakerViewSet, self).post(request, *args, **kwargs)
        return response
