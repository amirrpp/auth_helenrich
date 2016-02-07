import weblayout.models as wlm


def main_menu(request):
    """
    Ensure that the search form is available site wide
    """
    return {'main_menu': wlm.MainMenu.objects.all(), }
