from django.http import HttpResponse, JsonResponse


def index(request):
    html = "<html><body>Hi there, nothing to see here, come back later.</body></html>"
    return HttpResponse(html)


def health_check(request):
    return JsonResponse({"message": "All good"})


def ping(request):
    return JsonResponse({"message": "pong"})
