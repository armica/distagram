# django form
# 원칙적으로 form 태그는 html -> django form을 사용하면 modelform 해당 모델에 있는 필드
# 필드에 적절한 form tag를 찾아서 html을 만들어 준다.

from django.contrib.auth.models import User
from django import forms
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reset Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        # clean_form
        # clean_fieldName
        def clean_password2(self):
            cd = self.cleaned_data
            print(cd)
            if cd['password2'] != cd['password']:
                raise forms.ValidationError('Password doesn\t match.')
            return cd['password2']