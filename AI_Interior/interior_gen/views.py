import os

from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .forms import ImageGenForm
from .utils import build_payload
from .tasks import generate_image_task
from celery.result import AsyncResult

class UploadPageView(TemplateView):
    template_name = 'interior_gen/simple_upload.html'

@method_decorator(csrf_exempt, name="dispatch")
class GenerateImageView(View):
    @staticmethod
    def post(request):
        form = ImageGenForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({'error': form.errors}, status=400)

        image_input = form.cleaned_data['image']
        if hasattr(image_input, 'chunks'):
            temp_dir = 'media/temp'
            os.makedirs(temp_dir, exist_ok=True)

            filename = image_input.name
            temp_path = os.path.join(temp_dir, filename)
            with open(temp_path, 'wb') as f:
                for chunk in image_input.chunks():
                    f.write(chunk)

            image_url = temp_path
        else:
            image_url = image_input

        prompt  = form.cleaned_data['prompt']

        payload = build_payload(
            image_url=image_url,
            prompt=prompt,
        )
        task = generate_image_task.apply_async(args=[payload])

        return JsonResponse({'task_id': task.id}, status=202)

    @staticmethod
    def get():
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class ImageStatusView(View):
    @staticmethod
    def get(request):
        task_id = request.GET.get('task_id')
        if not task_id:
            return JsonResponse({'error': 'task_id required'}, status=400)

        result = AsyncResult(task_id)
        state = result.state
        if state in ('PENDING',):
            return JsonResponse({'status': 'pending'})
        if state in ('RETRY','STARTED'):
            return JsonResponse({'status': 'in progress'})
        if state == 'FAILURE':
            return JsonResponse({'status': 'error', 'msg': str(result.result)})
        return JsonResponse({'status': 'succeeded', 'url': result.result})


