from django.contrib import admin
from .models import Article,Category
# Register your models here.

admin.site.site_header = "مدیریت وبلاگ بیت رایت"

def make_published(modeladmin, request, queryset):
    row_updated = queryset.update(status='p')
    message_bit = 'منتشر شد'
    modeladmin.message_user(request,"{} مقاله {}".format(row_updated, message_bit))
make_published.short_description = 'انتشار مقالات'

def make_draft(modeladmin, request, queryset):
    row_updated = queryset.update(status='d')
    message_bit = 'پیش نویس شد'
    modeladmin.message_user(request,"{} مقاله {}".format(row_updated, message_bit))
make_draft.short_description = 'پیش نویس مقالات'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ('treeshow','status')
    list_filter = (['status'])
    search_fields = ('title','slug')
    prepopulated_fields = {'slug':('title',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin): 
    list_display = ('title', 'jpublished_at','status','author','category_to_str')
    list_filter = ('published_at','status','author')
    search_fields = ('title','description')
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status', '-published_at']
    actions = [make_published, make_draft]


