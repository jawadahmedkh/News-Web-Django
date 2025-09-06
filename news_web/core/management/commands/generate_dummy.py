from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils import timezone
from core.models import Category, News, Ad
import requests
import random

class Command(BaseCommand):
    help = "Generate dummy categories, news, and ads with images"

    def handle(self, *args, **kwargs):
        # Ensure admin user
        user, created = User.objects.get_or_create(username="admin")
        if created:
            user.set_password("admin123")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Created default admin user (admin/admin123)"))

        # Categories
        category_names = ["سیاست", "کھیل", "ٹیکنالوجی", "صحت", "تعلیم"]
        categories = []
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories."))

        # Placeholder image
        img_url = "https://via.placeholder.com/600x400.png?text=Dummy+Image"
        response = requests.get(img_url)
        image_file = ContentFile(response.content, name="dummy.png")

        # News
        for i in range(10):
            category = random.choice(categories)
            news = News.objects.create(
                title=f"ڈمی خبر {i+1}",
                content=f"<p>یہ ایک ڈمی خبر {i+1} ہے جو ٹیسٹنگ کے لئے بنائی گئی ہے۔</p>",
                category=category,
                author=user,
                status="published",
            )
            news.image.save(f"news_{i+1}.png", image_file, save=True)
        self.stdout.write(self.style.SUCCESS("Created 10 dummy news articles."))

        # Ads
        ad_img_url = "https://via.placeholder.com/300x200.png?text=Ad"
        ad_response = requests.get(ad_img_url)
        ad_image_file = ContentFile(ad_response.content, name="ad.png")

        for i in range(3):
            ad = Ad.objects.create(
                title=f"اشتہار {i+1}",
                link="https://example.com",
                start_date=timezone.now().date(),
                end_date=(timezone.now() + timezone.timedelta(days=30)).date(),
                is_active=True,
            )
            ad.image.save(f"ad_{i+1}.png", ad_image_file, save=True)
        self.stdout.write(self.style.SUCCESS("Created 3 dummy ads."))
