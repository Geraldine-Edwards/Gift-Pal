from django.shortcuts import render


def home(request):
    return render(request, 'index.html')

def learn_more(request):
    return render(request, 'learn_more.html')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def site_map(request):
    return render(request, 'sitemap.html')
