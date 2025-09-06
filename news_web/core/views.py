from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import News, Category, Ad


# =========================
# Public Views
# =========================
def home(request):
    categories = Category.objects.all()
    news_list = News.objects.filter(status="published").order_by("-created_at")[:10]

    # only running ads
    ads = Ad.objects.filter(is_active=True)
    ads = [ad for ad in ads if ad.is_running()]

    return render(request, "core/home.html", {
        "categories": categories,
        "news_list": news_list,
        "ads": ads,
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


def ads_list(request):
    ads = Ad.objects.filter(is_active=True)
    ads = [ad for ad in ads if ad.is_running()]
    return render(request, "core/ads_list.html", {"ads": ads})


def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug, is_active=True)
    return render(request, "core/ad_detail.html", {"ad": ad})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


# =========================
# Admin Dashboard
# =========================
def admin_dashboard(request):
    news_count = News.objects.count()
    category_count = Category.objects.count()
    ad_count = Ad.objects.count()
    return render(request, "core/admin_dashboard.html", {
        "news_count": news_count,
        "category_count": category_count,
        "ad_count": ad_count,
    })


# =========================
# Admin - News CRUD
# =========================
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
        news.category = Category.objects.filter(slug=category_slug).first()
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


# =========================
# Admin - Ads CRUD
# =========================
def admin_ads_list(request):
    ads = Ad.objects.all()
    return render(request, "core/admin_ads_list.html", {"ads": ads})


def admin_ads_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        link = request.POST.get("link")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        image = request.FILES.get("image")

        Ad.objects.create(
            title=title,
            link=link,
            start_date=start_date,
            end_date=end_date,
            image=image,
        )
        return redirect("admin_ads_list")
    return render(request, "core/admin_ads_form.html")


def admin_ads_edit(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.method == "POST":
        ad.title = request.POST.get("title")
        ad.link = request.POST.get("link")
        ad.start_date = request.POST.get("start_date")
        ad.end_date = request.POST.get("end_date")
        if request.FILES.get("image"):
            ad.image = request.FILES.get("image")
        ad.is_active = request.POST.get("is_active") == "on"
        ad.save()
        return redirect("admin_ads_list")
    return render(request, "core/admin_ads_form.html", {"ad": ad})


def admin_ads_delete(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    ad.delete()
    return redirect("admin_ads_list")
