from django.shortcuts import render


def menu(request, title=None, item_path=None):
    template = 'base.html'
    return render(request, template)
