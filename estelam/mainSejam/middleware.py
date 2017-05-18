from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
import khayyam


class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return None

    try:
      if khayyam.JalaliDatetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass

    request.session['last_touch'] = khayyam.JalaliDatetime.now()