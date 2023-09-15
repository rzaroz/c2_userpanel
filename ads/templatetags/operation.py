from django import template

register = template.Library()


@register.filter(name="rename_media_url")
def rename_media_url(url):
    newUrl = url.replace("media", "add_media")
    return newUrl
