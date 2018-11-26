from django.contrib import admin
from .models import Photo
# Register your models here.

from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    # 관리자 페이지 옵션 클래스
    list_display = ['id', 'author', 'created', 'updated'] # 목록에서 어떤 내용을 보여줄 지 필드 값 설정
    list_filter = ['author', 'created', 'updated'] # 필터 기능 추가
    search_fields = ['text', 'created'] # Foreign Key 필트는 사용 금지
    raw_id_fields = ['author']
    ordering = ['-updated', '-created'] #

admin.site.register(Photo, PhotoAdmin) # Photo 라는 모델을 관리자 페이지에서 어떻게 보여줄 것이냐
