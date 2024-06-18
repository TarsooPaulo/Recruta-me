from django.utils import timezone
from django.contrib.sessions.models import Session

def online_users(request):
    online_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    online_users = []

    for session in online_sessions:
        data = session.get_decoded()
        online_users.append(data.get('_auth_user_id', None))

    online_users = set(online_users)
    return {'online_users_count': len(online_users)}