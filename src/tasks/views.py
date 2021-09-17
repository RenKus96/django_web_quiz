from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from celery.result import AsyncResult

from tasks.sample_tasks import create_task


# @cache_page(timeout=(60 * 15), cache='my_cache')
# @cache_page(timeout=(60))
def home(request):
    return render(request, "tasks/tasks.html")


@csrf_exempt
def run_task(request):
    if request.POST:
        task_type = request.POST.get("type")
        task = create_task.delay(task_type)
        return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_status(request, task_id):
    if request.method == 'GET':
        task_result = AsyncResult(task_id)

        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": str(task_result.result)
        }
        return JsonResponse(result, status=200)
