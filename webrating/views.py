from django.shortcuts import render
from webrating.models import Rating

import weblayout.models as wlm
import website.models as wsm
import webform.forms as wff
from django.http import Http404


def comments(request):
    try:
        # System Elements:
        sys_elem = wlm.SystemElement.objects.all()
        sys_header = sys_elem.filter(name='Header').first()
        sys_footer = sys_elem.filter(name='Footer').first()
        sys_script = sys_elem.filter(name='Script').first()

        # Banners:
        all_banners = wsm.Banner.objects.all()
        image_positions = wsm.Banners()
        if all_banners:
            for banner in all_banners:
                image_position = wsm.BannerImagePosition.objects.filter(banner=wsm.Banner.objects.filter(
                    name=banner.name).first()).all()
                image_positions.append(banner.name, image_position)

        ratings = Rating.objects.order_by('-date_on_add').all()

        if request.POST:
            result, form = wff.FormRatingGlobal.process(request)
            if result:
                pass
        else:
            form = wff.FormRatingGlobal()

        return render(request, 'comments.html', {
            'main_menu': wlm.MainMenu.objects.all(),
            'additional_menu': wlm.AdditionalMenu.objects.all(),
            'extra_menu': wlm.ExtraMenu.objects.all(),
            'sys_header': sys_header,
            'sys_footer': sys_footer,
            'sys_script': sys_script,
            'banners': image_positions,
            'ratings': ratings,
            'form_rating': form
        })
    except:
        raise Http404('Page not found')
