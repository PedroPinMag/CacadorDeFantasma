# public/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .location_store import update_user_location


@csrf_exempt  # For simplicity in this example; consider CSRF protection for production
@require_POST
def api_update_location(request):
    try:
        data = json.loads(request.body)
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        device_id = data.get('deviceId')  # Ensure your frontend sends this

        if None in [latitude, longitude, device_id]:
            return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

        update_user_location(device_id, latitude, longitude)
        return JsonResponse({'status': 'success', 'message': 'Location updated'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid latitude or longitude'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


from .services import determine_fantasminha_locations # Assuming the above function is in services.py

def api_get_fantasminha_locations(request):
    data = determine_fantasminha_locations()
    return JsonResponse(data)
# We'll add the view for the main page and the API to get bus locations later
from django.shortcuts import render

# Create your views here.
# public/views.py (add this view)
from django.shortcuts import render

def fantasminha_tracker_page(request):
    return render(request, 'public/fantasminha_map.html')