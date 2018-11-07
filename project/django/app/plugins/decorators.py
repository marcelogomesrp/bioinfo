from django.shortcuts import redirect
from enrollments.models import Enrollment


def plugin_enrollment_required(f):
    def wrap(request, *args, **kwargs):
        class_enrollment = Enrollment.approved.filter(user=request.user).get(id=kwargs['classenrollment_id'])
        try:
            plugin_enrollment = class_enrollment.pluginenrollment_set.all()[0]
        except:
            next_urls = []
            for p in class_enrollment.course_class.active_plugins:
                if hasattr(p, 'enrollment_url') and p.enrollment_url:
                    next_urls.append(p.enrollment_url)
            if next_urls:
                return redirect(next_urls.pop(0), classenrollment_id=class_enrollment.id)
        return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
    return wrap
