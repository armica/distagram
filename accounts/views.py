from django.shortcuts import render

# Todo register view
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        # 회원가입 정보 입력 후
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # 비밀번호 암호화
            b = new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        # 회원가입 정보 입력 할 때
        user_form = RegisterForm()
    return render(request, 'registration/register.html', {'form':user_form})