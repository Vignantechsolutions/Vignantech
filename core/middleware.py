import traceback
from django.http import HttpResponse

class DebugExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if request.GET.get('debug') == '1':
            tb_text = traceback.format_exc()
            return HttpResponse(tb_text, status=500, content_type="text/plain; charset=utf-8")
        return None
