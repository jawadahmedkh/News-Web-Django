from django import forms
from .models import News, Category

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "category", "content", "image", "status"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
