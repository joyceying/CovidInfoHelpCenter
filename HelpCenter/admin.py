from django.contrib import admin
# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from HelpCenter.models import User,reportDetail
from HelpCenter.utils import encrypt

# Register your models here.
admin.site.site_header='covidCenter'
admin.site.site_title='covidCenter admin management'


class NormalUserInfoAdmin(admin.ModelAdmin):
    list_display=["name","password"]       ##设置显示的字段

    search_fields = ('name',)
    list_editable = ()

class reportdetaillist(admin.ModelAdmin):
    list_display = ["name", "closeContact", "symptoms", "date", "image"]

    search_fields = ('name',)






##在admin中注册绑定
admin.site.register(User,NormalUserInfoAdmin)
admin.site.register(reportDetail, reportdetaillist)