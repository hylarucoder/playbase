def get_domain(request):
    return request.headers.get("Host")
