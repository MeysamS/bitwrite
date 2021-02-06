
from django import template
from ..models import Article, Category
register = template.Library()


@register.inclusion_tag("blog/partials/category-navbar.html")
def category_navbar():
    return {
        'categories': Category.objects.filter(status=True)
    }


@register.inclusion_tag("blog/partials/article_featured.html")
def articles_featured():
    return {
        'object': Article.objects.filter(status='p').order_by('-published_at').first()
    }
