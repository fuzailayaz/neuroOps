from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def redis_manage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            key = data.get('key')
            value = data.get('value')
            ttl = data.get('ttl', 300)  # Default TTL: 5 minutes
            
            if not key or value is None:
                return JsonResponse({'error': 'Both key and value are required'}, status=400)
                
            cache.set(key, value, timeout=ttl)
            return JsonResponse({'status': 'success', 'message': f'Set {key} in Redis'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # GET request - list all keys or get a specific key
    key = request.GET.get('key')
    if key:
        value = cache.get(key)
        if value is None:
            return JsonResponse({'error': 'Key not found'}, status=404)
        return JsonResponse({'key': key, 'value': value})
    
    # List all keys (Note: Use with caution in production with large datasets)
    keys = cache.keys('*')
    data = {k: cache.get(k) for k in keys}
    return JsonResponse(data)

@csrf_exempt
@require_http_methods(["DELETE"])
def redis_delete(request, key):
    deleted = cache.delete(key)
    if deleted:
        return JsonResponse({'status': 'success', 'message': f'Deleted key: {key}'})
    return JsonResponse({'error': 'Key not found'}, status=404)


class RedisManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/redis_management.html'
