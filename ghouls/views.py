from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from users.utils import scores_token
from .forms import *
from .models import *
from django.db.models import Q

class UserListView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request=request, 
            template_name="ghouls/userlist.html",
            context={
                "users": get_user_model().objects.all(), 
                "form": FindUserForm(),
                }
            )

    def post(self, request, *args, **kwargs):
        if FindUserForm(request.POST).is_valid():
            search_name = request.POST['name']
            users = get_user_model().objects.all().filter(first_name__icontains = search_name).order_by(request.POST['order'])
        else:
            users = get_user_model().objects.all()

        return render(
            request=request, 
            template_name="ghouls/userlist.html",
            context={
                "users": users, 
                "form": FindUserForm(request.POST),
                }
            )


class LevelUpView(TemplateView):
    template_name = "ghouls/levelUp.html"


class LevelUpUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.zxc_scores <= 0:
            user.zxc_scores = 1000
            user.zxc_level += 1
            user.save()
            return redirect(reverse_lazy("user_list"))
        else:
            return redirect(reverse_lazy("user_list"))

    def test_func(self):
        owner = get_user_model().objects.get(pk=self.kwargs["pk"])
        return self.request.user == owner


class GrindView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name="ghouls/grind.html", context={'token': scores_token.make_token(request.user), 'pk': request.user.pk, 'scores': request.user.zxc_scores})

    def test_func(self):
        return self.request.user.active_email


class ExitGrindView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=kwargs["pk"])
        user.zxc_scores -= int(kwargs['scores'])
        user.save()
        return redirect(reverse_lazy('user_list'))

    def test_func(self):
        owner = get_user_model().objects.get(pk=self.kwargs["pk"])
        return scores_token.check_token(self.request.user, self.kwargs['token']) and self.request.user == owner


class SendFriendInviteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        try:
            send_to = get_user_model().objects.get(pk=kwargs['pk'])
        except get_user_model().DoesNotExist:
            return JsonResponse({'message': 'User does not exist'}, status=205)

        if send_to == request.user:
            return JsonResponse({'message': 'Your cant send invite yourself'}, status=200)

        exist1 = None
        exist2 = None

        try:
            exist1 = FriendList.objects.get(user_one=request.user, user_two=send_to)
        except FriendList.DoesNotExist:
            pass

        try:
            exist2 = FriendList.objects.get(user_one=send_to, user_two=request.user)
        except FriendList.DoesNotExist:
            pass

        if(exist1 != None or exist2 != None):
            return JsonResponse({'message': 'You or your friend already send invite'}, status=200)
        else:
            FriendList.objects.create(user_one=request.user, user_two=send_to, approved_one=True)
            return JsonResponse({'message': f'Your invite was sended {exist1} {exist2}'}, status=200)   


class UserInvitesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=kwargs['pk'])
        
        friends = []
        friends_objects = FriendList.objects.all().filter(Q(user_one=user, approved_one=True, approved_two=True) | Q(user_two=user, approved_one=True, approved_two=True))

        invite_users = []
        invites = FriendList.objects.all().filter(Q(user_one=user, approved_one=False) | Q(user_two=user, approved_two=False))

        for i in invites:
            if i.user_one == user:
                invite_users.append(i.user_two)
            elif i.user_two == user:
                invite_users.append(i.user_one)

        for i in friends_objects:
            if i.user_one == user:
                friends.append(i.user_two)
            else:
                friends.append(i.user_one)

        
        return render(request=request, template_name='ghouls/invites.html', context={'invite_users': invite_users, 'users': friends})


    def test_func(self):
        owner = get_user_model().objects.get(pk=self.kwargs["pk"])
        return self.request.user == owner


class ApprovedInviteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        invite = None
        user = request.user
        recipient = get_user_model().objects.get(pk=kwargs['pk'])

        try:
            invite = FriendList.objects.get(user_one=user, user_two=recipient, approved_one=False, approved_two=True)
        except FriendList.DoesNotExist:
            pass

        try:
            invite = FriendList.objects.get(user_two=user, user_one=recipient, approved_two=False, approved_one=True)
        except FriendList.DoesNotExist:
            pass

        if invite == None:
            return redirect(reverse_lazy('user_list'))
        elif invite.approved_one == False:
            invite.approved_one = True
        else:
            invite.approved_two = True

        invite.save()
        return redirect(reverse_lazy('user_invites', kwargs={'pk':user.pk}))

class RejectInviteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        invite = None
        user = request.user
        recipient = get_user_model().objects.get(pk=kwargs['pk'])

        try:
            invite = FriendList.objects.get(user_one=user, user_two=recipient, approved_one=False, approved_two=True)
        except FriendList.DoesNotExist:
            pass

        try:
            invite = FriendList.objects.get(user_two=user, user_one=recipient, approved_two=False, approved_one=True)
        except FriendList.DoesNotExist:
            pass

        if invite == None:
            return redirect(reverse_lazy('user_list'))
        else:
            invite.delete()

        return redirect(reverse_lazy('user_invites', kwargs={'pk':user.pk}))