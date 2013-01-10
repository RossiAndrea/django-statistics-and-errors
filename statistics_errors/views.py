from django.http import HttpResponse
from django.core.exceptions import DatabaseError, IntegrityError

from client_errors.models import UserError

def _ip_address_finder(request, fallback = None):
    return request.META.get('HTTP_X_FORWARDED_FOR',
                request.META.get('REMOTE_ADDR', None))

def error(request, *args, **kwargs):
    data = request.GET.copy()
    if request.method == 'POST':
        data = request.POST.copy()

    user = None
    if request.user.is_authenticated():
        user = request.user

    try:
        UserError.objects.create(
            created_by = user,
            message    = data.get('msg'),
            url        = data.get('url'),
            loc        = data.get('loc'),
            os         = data.get('os'),
            browser    = data.get('bw'),
            version    = data.get('vs'),
            device     = data.get('device'),
            plugins    = data.get('plugins'),
            locale     = data.get('locale'),
            address    = _ip_address_finder(request),
        )
        return HttpResponse(status=200)
    except (DatabaseError, IntegrityError):
        return HttpResponse(status=500)
