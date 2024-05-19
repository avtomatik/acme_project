from django.shortcuts import render


def homepage(request):
    template_name = 'pages/index.html'
    return render(request, template_name)
