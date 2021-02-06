from django.db import models
from django.utils import timezone
from apps.account.models import User
from django.urls import reverse
from extensions.myjalali import jalali_converter
from ckeditor.fields import RichTextField
# Create your models here.


class ArticleMAnager(models.Manager):
    def published(self):
        return self.filter(status='p').order_by('-published_at')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="children", verbose_name="زیر دسته")
    title = models.CharField(max_length=200, verbose_name="دسته بندی")
    slug = models.SlugField(max_length=250, unique=True,
                            verbose_name="آدرس دسته بندی")
    status = models.BooleanField(
        default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField()

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    objects = CategoryManager()

    def __str__(self):
        return self.title

    def treeshow(self):
        full_path = [self.title]

        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),      # draft
        ('p', 'منتشر شده'),     # published
        ('i', 'در حال بررسی'),  # investigation
        ('b', 'برگشت خورده'),         # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name="articles", verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=250, unique=True,
                            verbose_name="آدرس سئو")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name="articles")
    description = RichTextField()
    thumbnail = models.ImageField(upload_to="images", verbose_name="تصویر",blank=True, null=True)
    published_at = models.DateTimeField(
        default=timezone.now, verbose_name="زمان انتشار")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(
        default=False, verbose_name="مقاله ویژه")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت نمایش")

    def get_absolute_url(self):
        return reverse("account:home")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def jpublished_at(self):
        return jalali_converter(self.published_at)
    jpublished_at.short_description = "زمان انتشار"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی ها"

    objects = ArticleMAnager()
