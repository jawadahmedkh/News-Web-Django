from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, null=True, default=None)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class News(models.Model):
    STATUS_CHOICES = (
        ('draft', 'ڈرافٹ'),
        ('published', 'شائع شدہ'),
    )

    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news_articles", verbose_name="مصنف")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="news_articles", verbose_name="زمرہ")
    short_description = models.CharField(max_length=300, verbose_name="خلاصہ", blank=True, null=True)
    content = HTMLField(verbose_name="مواد")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تخلیق")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ تازہ کاری")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="حالت")
    views = models.PositiveIntegerField(default=0, verbose_name="ناظرین")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "خبر"
        verbose_name_plural = "خبریں"

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})
