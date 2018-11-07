from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from models import Enrollment


def class_enrollment_required(f):
    def wrap(request, *args, **kwargs):
        try:
            class_enrollment = Enrollment.objects.filter(user=request.user).get(id=kwargs['classenrollment_id'])
        except Enrollment.DoesNotExist:
            messages.error(request, _('You are not currently enrolled in this class'))
            return redirect('home')
        
        if not class_enrollment.is_approved:
            messages.error(request, _('Your subscription is waiting for approval'))
            return redirect('home')
            #return redirect('pending_approval')
        return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
    return wrap