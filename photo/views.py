from django.shortcuts import render
from .models import Photo
# Create your views here.
# 데코레이터(함수형뷰), 믹스인(클래스형뷰)
# 부가 기능 - 함수를 실행하기 전에 추가로 실행하고 싶은 일이 있을 때

# 접근 권한 제어 ;
# 1. 코드로 하는 방법
# 2. 데코레이트, 믹스인
# 3. 앱을 사용
# 4. 권한 생성 추가
# 5. 관리자에서 권한 관리

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos':photos})


from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
# 디테일 뷰
class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/detail.html'

class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'photo/upload.html'
    fields = ['image', 'text', 'tag']

    def form_valid(self, form):
        # 작성자 설정
        form.instance.author_id = self.request.user.id
        # 작성시간 - model
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

from django.views.generic.edit import UpdateView, DeleteView
class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields =  ['image', 'text', 'tag']
    template_name = 'photo/update.html'
    # success_url - 글쓰기, 수정, 삭제 => 해당 모델의 get_absolute_url 메소드
from django.http import HttpResponseRedirect # 301 리다이렉트 코드를 응답
from django.contrib import messages # 장고 어플리케이션 전체에 오류 메시지 등을 공유

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            # 지울 권한이 없다는 오류메시지를 컨텍스트로 전달
            # messages.warning(request, "You do not have permjission for deleting this photo.")
            # 1. raise 오류를 발생시킨다.
            # 2. get method의 파라미터로 메시지를 전달
            # 원래 페이지로 리턴
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDeleteView, self).get(request, *args, **kwargs)

# 시그널이라는 것을 사용해서 글이 삭제 된 후에 이미지를 삭제
from django.db.models.signals import post_delete
from django.dispatch import receiver
@receiver(post_delete, sender=Photo)
def post_delete(sender, instance, **kwargs):
    storage, path = instance.image.storage, instance.image.path
    if (path!='.') and (path!='/') and (path!='photos/') and (path!='photos/.'):
        storage.delete(path)

# disqus.com : 댓글시스템
# heroku.com : 배포 / CLI 깔아오기
# aws.amazon.com : s3 서비스, 최종 배포


from tagging.views import TaggedObjectList
class TaggedPhotoList(TaggedObjectList):
    model = Photo
    template_name = 'photo/tagged_photo_list.html'