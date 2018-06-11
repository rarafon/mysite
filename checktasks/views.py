from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Task, DateRecord
import datetime

def view_tasks(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    tasks_list = get_tasks(request.user)

    return render(
        request,
        "checktasks/view.html",
        {
            "tasks": tasks_list,
        }
    )

def get_tasks(user):
    """
    Retrieves all of the tasks for a particular user.
    :param user: request.user
    :return: lists containing all of Tasks for that user
    """
    tasks_list = []
    tasks = Task.objects.filter(user=user)

    for task in tasks:
        task = {}
        tasks_list.append(task)

    return tasks_list

def add(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get("name")
        task = Task(name=name, user=user)
        task.save()

        return JsonResponse({"name": name})

    return JsonResponse({})

def ajax_tasks(request):
    """
        Retrieves all of the tasks for a particular user.
        :param user: request.user
        :return: lists containing all of Tasks for that user
    """

    tasks_list = []
    user = request.user
    tasks = Task.objects.filter(user=user)

    start_year = int(request.POST.get("start_year"))
    end_year = int(request.POST.get("end_year"))
    start_month = int(request.POST.get("start_month"))
    end_month = int(request.POST.get("end_month"))
    start_day = int(request.POST.get("start_day"))
    end_day = int(request.POST.get("end_day"))

    print(end_year, end_month, end_day)

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)

    for task in tasks:
        dates_dic = {}

        dates_q = DateRecord.objects.filter(task=task).filter(date__gte=start_date,
                                                              date__lte=end_date)
        for d in dates_q:
            date_string = str(d)
            dates_dic[date_string] = 1

        tasks_list.append({
            "taskName": task.name,
            "type": task.type,
            "dates": dates_dic,
        })

    return JsonResponse(tasks_list, safe=False)


def click_task_ajax(request):
    taskName = request.POST.get("task")
    year = int(request.POST.get("year"))
    month = int(request.POST.get("month"))
    day = int(request.POST.get("day"))

    dateRecord = DateRecord.get_DateRecord(year,month,day)

    task = Task.objects.get(name=taskName)

    return JsonResponse({
        "task": taskName,
        "year": year,
        "month": month,
        "day": day,
        "d": str(dateRecord),
    })