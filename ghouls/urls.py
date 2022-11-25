from django.urls import path
from .views import *

urlpatterns = [
    path('levelUp/', LevelUpView.as_view(), name="levelUp"),
    path('levelUp/<pk>/', LevelUpUserView.as_view(), name="levelUp_user"),
    path('grind/', GrindView.as_view(), name="grind"),
    path('grind/<pk>/<token>/<scores>/', ExitGrindView.as_view(), name='grind_exit'),
    path('invites/<pk>/', UserInvitesView.as_view(), name="user_invites"),
    path('addfriend/approved/<pk>/', ApprovedInviteView.as_view(), name="approved_friend_invite"),
    path('addfriend/reject/<pk>/', RejectInviteView.as_view(), name="reject_friend_invite"),
    path('addfriend/<pk>/', SendFriendInviteView.as_view(), name="send_friend_invite"),
    path('', UserListView.as_view(), name="user_list"),
]
