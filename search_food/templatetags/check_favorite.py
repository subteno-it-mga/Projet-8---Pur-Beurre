from django.template.defaulttags import register


@register.simple_tag
def check_favorite(barcode, user):
    from ..models import Favorite
    from django.contrib.auth.models import User

    find_user = User.objects.filter(username=user)
    check_fav = Favorite.objects.filter(
        user_associate__in=find_user, barcode=barcode)

    if check_fav:
        return True
    else:
        return False
