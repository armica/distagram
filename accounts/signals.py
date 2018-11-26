from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

def naver_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.get(user=user)
    user.last_name = social_user.extra_data['name']
    user.save()

#시그널과 해당 함수를 connect
user_signed_up.connect(naver_signup)