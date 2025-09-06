from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse



# =========================
# Public Views
# =========================
def home(request):
    categories = Category.objects.all()
    news_list = News.objects.filter(status="published").order_by("-created_at")[:10]

    return render(request, "core/home.html", {
        "categories": categories,
        "news_list": news_list,
        })


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status="published")
    news.views += 1
    news.save()
    return render(request, "core/news_detail.html", {"news": news})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "core/category_list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_list = News.objects.filter(category=category, status="published")
    return render(request, "core/category_detail.html", {
        "category": category,
        "news_list": news_list,
    })



def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


# Admin check function
# Admin check function
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Custom Login View
class AdminLoginView(LoginView):
    template_name = 'core/admin_login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('admin_dashboard')

# Logout view
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Update admin_dashboard to remove ad_count
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    news_count = News.objects.count()
    category_count = Category.objects.count()
    latest_news = News.objects.all().order_by('-created_at')[:5]
    
    return render(request, "core/admin_dashboard.html", {
        "news_count": news_count,
        "category_count": category_count,
        "latest_news": latest_news,
    })


# =========================
# Admin - News CRUD
# =========================
@login_required
@user_passes_test(is_admin)
def admin_news_list(request):
    news_list = News.objects.all()
    return render(request, "core/admin_news_list.html", {"news_list": news_list})


def admin_news_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_slug = request.POST.get("category")
        category = Category.objects.filter(slug=category_slug).first()
        image = request.FILES.get("image")

        News.objects.create(
            title=title,
            content=content,
            category=category,
            image=image,
            author=request.user,
            status=request.POST.get("status", "draft"),
        )
        return redirect("admin_news_list")

    categories = Category.objects.all()
    return render(request, "core/admin_news_form.html", {"categories": categories})


def admin_news_edit(request, slug):
    news = get_object_or_404(News, slug=slug)
    if request.method == "POST":
        news.title = request.POST.get("title")
        news.content = request.POST.get("content")
        category_slug = request.POST.get("category")
        category = Category.objects.filter(slug=category_slug).first()
        if not category:
            categories = Category.objects.all()
            error_message = "Selected category is invalid."
            return render(
                request,
                "core/admin_news_form.html",
                {"news": news, "categories": categories, "error_message": error_message},
            )
        news.category = category
        if request.FILES.get("image"):
            news.image = request.FILES.get("image")
        news.status = request.POST.get("status", "draft")
        news.save()
        return redirect("admin_news_list")

    categories = Category.objects.all()
    return render(request, "core/admin_news_form.html", {"news": news, "categories": categories})


def admin_news_delete(request, slug):
    news = get_object_or_404(News, slug=slug)
    news.delete()
    return redirect("admin_news_list")


# =========================
# Admin - Category CRUD
# =========================
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, "core/admin_category_list.html", {"categories": categories})


def admin_category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Category.objects.create(name=name)
        return redirect("admin_category_list")
    return render(request, "core/admin_category_form.html")


def admin_category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("admin_category_list")
    return render(request, "core/admin_category_form.html", {"category": category})


def admin_category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect("admin_category_list")

