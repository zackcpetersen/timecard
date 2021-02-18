from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.serializers import UserCreationSerializer, UserUpdateSerializer
from accounts import constants as account_constants
from accounts.forms import ForgotPasswordForm, UserResetPasswordForm
from accounts.models import User
from accounts import permissions
from timecard.viewsets import AuthenticatedAPIViewSet


class UserMainViewSet(AuthenticatedAPIViewSet):
    """
    API Endpoint for User CRUD
    """
    permission_classes = [IsAuthenticated, permissions.IsSuperuser]

    queryset = User.objects.all()
    serializer_class = UserCreationSerializer


class UserUpdateViewSet(AuthenticatedAPIViewSet):
    permission_classes = [IsAuthenticated, permissions.ObjectOwnerOrSuperuserUpdate]

    queryset = User.objects.all().order_by('-pk')
    serializer_class = UserUpdateSerializer


class CurrentUserGetView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(status=200, data=serializer.data)


class UserResetPasswordView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = UserResetPasswordForm(request.data)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.pass_valid = True
            request.user.save()
            data = {'password': 'Password Successfully Changed'}
            return Response(status=200, data=data)
        return Response(status=400, data=form.errors)


class UserForgotPasswordView(views.APIView):

    def post(self, request):
        form = ForgotPasswordForm(request.data)
        if form.is_valid():
            user = form.cleaned_data['user']
            email_subj = account_constants.UPDATE_SUBJECT.format(user.first_name, user.last_name)
            User.objects.email_random_pass(user, email_subj)
            data = {
                'password': 'A temporary password has been sent to {}'.format(form.cleaned_data['email'])
            }
            return Response(status=200, data=data)
        return Response(status=400, data=form.errors)
