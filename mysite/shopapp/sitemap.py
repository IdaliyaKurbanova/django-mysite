from django.contrib.sitemaps import Sitemap

from shopapp.models import Product


class ShopSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Product.objects.filter(archived=False).all()

    def lastmod(self, item):
        return item.updated_at



