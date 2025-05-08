import time
from celery import shared_task
from .utils import post_interior, get_interior_status

@shared_task(rate_limit='5/m', bind=True, max_retries=3, default_retry_delay=10)
def generate_image_task(self, payload):
    try:
        data = post_interior(payload)
        task_id = data['id']

        while True:
            status = get_interior_status(task_id)['status']
            if status == 'succeeded':
                return get_interior_status(task_id)['output']
            if status == 'error':
                raise RuntimeError('API error')
            time.sleep(1)

    except Exception as exc:
        raise self.retry(exc=exc)
