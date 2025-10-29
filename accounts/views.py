from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import user_passes_test

from .models import Trial, CleaningRecord, ShiftMessage, ManagerMessage
from .models import CleaningTask
import json
from datetime import datetime


def user_has_dashboard_role(user):
    """Return True if the user is allowed to access the dashboard.

    Allowed roles: Admin, Administrator, Owner, Manager (also superusers).
    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    allowed = ['Admin', 'Administrator', 'Owner', 'Manager']
    return user.groups.filter(name__in=allowed).exists()


@require_http_methods(['POST'])
@login_required
def logout_view(request):
    """Log the user out and render a simple logout confirmation page.

    This view expects a POST (the UI sends a POST form). Using a dedicated view
    avoids redirects configured by LOGOUT_REDIRECT_URL and ensures the
    `accounts/logout.html` template is rendered.
    """
    logout(request)
    return render(request, 'accounts/logout.html', {})


@login_required
def dashboard_view(request):
    # Only allow users in certain groups to access the dashboard
    if not user_has_dashboard_role(request.user):
        # Render a simple 403 page for authenticated users without permission
        return HttpResponseForbidden(render(request, 'accounts/403.html', {}))

    user = request.user
    groups = user.groups.all()
    # Mock time-series data for preview (last 7 days)
    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # Registered trials per day (mock)
    registered = [12, 18, 9, 14, 20, 7, 16]
    # Converted trials per day (mock, <= registered)
    converted = [5, 9, 4, 7, 12, 2, 8]
    # Not converted = registered - converted
    not_converted = [r - c for r, c in zip(registered, converted)]

    import json
    context = {
        'user': user,
        'groups': groups,
        'chart_labels': json.dumps(labels),
        'registered': registered,
        'converted': json.dumps(converted),
        'not_converted': json.dumps(not_converted),
        'registered_sum': sum(registered),
        'converted_sum': sum(converted),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def overlevering_view(request):
    """Placeholder page for Overlevering. Main content intentionally minimal with dummy text for testing."""
    return render(request, 'accounts/overlevering.html', {'user': request.user, 'is_manager': _is_manager(request.user)})


@login_required
def post_login_redirect(request):
    """Redirect users after login based on their role.

    Receptionists -> Overlevering
    Managers/Owners/Admins -> Dashboard
    Fallback -> Overlevering if authenticated
    """
    user = request.user
    # superuser and dashboard-role users go to dashboard
    if user.is_superuser or user.groups.filter(name__in=['Admin','Administrator','Owner','Manager']).exists():
        return redirect('dashboard')

    # receptionists should land on overlevering
    if user.groups.filter(name='Receptionist').exists():
        return redirect('overlevering')

    # default fallback
    return redirect('overlevering')


@login_required
def cleaning_view(request):
    """Placeholder page for Rengøring accessible to all authenticated users."""
    return render(request, 'accounts/cleaning.html', {})


def _is_manager(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=['Manager','Owner','Admin','Administrator']).exists()


@login_required
def api_day_data(request):
    """Return JSON data for a given date passed as ?date=YYYY-MM-DD"""
    date_str = request.GET.get('date')
    if not date_str:
        return HttpResponseBadRequest('Missing date')
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest('Invalid date')

    trials = Trial.objects.filter(date=date).order_by('time')
    trials_list = [t.to_dict() for t in trials]

    cleaning = None
    try:
        cleaning = CleaningRecord.objects.get(date=date)
        cleaning = cleaning.to_dict()
    except CleaningRecord.DoesNotExist:
        cleaning = {'date': date.isoformat(), 'arrived': None, 'left': None}

    shift_msg = None
    try:
        sm = ShiftMessage.objects.get(date=date)
        shift_msg = sm.to_dict()
    except ShiftMessage.DoesNotExist:
        shift_msg = {'date': date.isoformat(), 'message': None}

    mgr_msg = None
    try:
        mm = ManagerMessage.objects.get(date=date)
        mgr_msg = mm.to_dict()
    except ManagerMessage.DoesNotExist:
        mgr_msg = {'date': date.isoformat(), 'message': None, 'reply': None}

    return JsonResponse({'trials': trials_list, 'cleaning': cleaning, 'shift_message': shift_msg, 'manager_message': mgr_msg})


@require_http_methods(['GET','POST'])
@login_required
def api_cleaning_tasks(request):
    """GET: ?weekday=0-6 returns tasks for that weekday. POST: create a new task (weekday, time, area, title, details, status).
    """
    if request.method == 'GET':
        wk = request.GET.get('weekday')
        try:
            wk = int(wk) if wk is not None else None
        except Exception:
            wk = None
        if wk is None:
            return HttpResponseBadRequest('Missing weekday')
        tasks = CleaningTask.objects.filter(weekday=wk).order_by('time', 'id')
        return JsonResponse({'tasks': [t.to_dict() for t in tasks]})

    # POST -> create
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    weekday = payload.get('weekday')
    try:
        weekday = int(weekday)
    except Exception:
        return HttpResponseBadRequest('Invalid weekday')
    t = CleaningTask.objects.create(
        weekday=weekday,
        time=payload.get('time',''),
        area=payload.get('area',''),
        title=payload.get('title',''),
        details=payload.get('details',''),
        status=payload.get('status','Pending')
    )
    return JsonResponse({'task': t.to_dict()})


@require_http_methods(['PUT','PATCH','DELETE'])
@login_required
def api_modify_cleaning_task(request, pk):
    try:
        task = CleaningTask.objects.get(pk=pk)
    except CleaningTask.DoesNotExist:
        return JsonResponse({'error':'not found'}, status=404)

    if request.method in ('PUT','PATCH'):
        try:
            payload = json.loads(request.body.decode())
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')
        # allow partial updates
        if 'status' in payload:
            task.status = payload.get('status')
        if 'time' in payload:
            task.time = payload.get('time','')
        if 'area' in payload:
            task.area = payload.get('area','')
        if 'title' in payload:
            task.title = payload.get('title','')
        if 'details' in payload:
            task.details = payload.get('details','')
        task.save()
        return JsonResponse({'task': task.to_dict()})

    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'deleted': True})


@require_http_methods(['POST'])
@login_required
def api_create_trial(request):
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    name = payload.get('name')
    trial_type = payload.get('trial_type')
    date_str = payload.get('date')
    if not (name and trial_type and date_str):
        return HttpResponseBadRequest('Missing fields')
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest('Invalid date')

    status = payload.get('status', 'Pending')
    reason = payload.get('reason')
    t = Trial.objects.create(name=name, trial_type=trial_type, date=date, created_by=request.user, status=status, reason=reason)
    return JsonResponse({'trial': t.to_dict()})


@require_http_methods(['PUT','PATCH','DELETE'])
@login_required
def api_modify_trial(request, pk):
    try:
        t = Trial.objects.get(pk=pk)
    except Trial.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    if request.method in ('PUT','PATCH'):
        try:
            payload = json.loads(request.body.decode())
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')
        name = payload.get('name')
        trial_type = payload.get('trial_type')
        status = payload.get('status')
        reason = payload.get('reason')
        if name:
            t.name = name
        if trial_type:
            t.trial_type = trial_type
        if status:
            t.status = status
            # clear reason if signed up
            if status != 'DidNotSignup':
                t.reason = ''
        if reason is not None:
            t.reason = reason
        t.save()
        return JsonResponse({'trial': t.to_dict()})

    if request.method == 'DELETE':
        t.delete()
        return JsonResponse({'deleted': True})


@require_http_methods(['POST'])
@login_required
def api_cleaning_update(request):
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    date_str = payload.get('date')
    arrived = payload.get('arrived')
    left = payload.get('left')
    if not date_str:
        return HttpResponseBadRequest('Missing date')
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest('Invalid date')

    obj, _ = CleaningRecord.objects.get_or_create(date=date)
    # parse times if provided
    def parse_time(t):
        if not t:
            return None
        try:
            return datetime.strptime(t, '%H:%M').time()
        except Exception:
            try:
                return datetime.strptime(t, '%H:%M:%S').time()
            except Exception:
                return None

    obj.arrived = parse_time(arrived)
    obj.left = parse_time(left)
    obj.save()
    return JsonResponse({'cleaning': obj.to_dict()})


@require_http_methods(['POST'])
@login_required
def api_shift_message(request):
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    date_str = payload.get('date')
    message = payload.get('message','')
    if not date_str:
        return HttpResponseBadRequest('Missing date')
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest('Invalid date')

    obj, _ = ShiftMessage.objects.get_or_create(date=date)
    obj.message = message
    obj.author = request.user
    obj.save()
    return JsonResponse({'shift_message': obj.to_dict()})


@require_http_methods(['POST'])
@login_required
def api_manager_message(request):
    try:
        payload = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    date_str = payload.get('date')
    message = payload.get('message','')
    reply = payload.get('reply')
    if not date_str:
        return HttpResponseBadRequest('Missing date')
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest('Invalid date')

    obj, _ = ManagerMessage.objects.get_or_create(date=date)
    # Any user can leave message, but only managers can set reply
    if message is not None:
        obj.message = message
        obj.author = request.user

    if reply is not None:
        # check manager permission
        if not _is_manager(request.user):
            return JsonResponse({'error':'forbidden'}, status=403)
        obj.reply = reply

    obj.save()
    return JsonResponse({'manager_message': obj.to_dict()})
