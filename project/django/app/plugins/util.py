from django.shortcuts import redirect
from enrollments.models import Enrollment

def get_class_enrollment(user, classenrollment_id):
    try:
        class_enrollment = Enrollment.objects.filter(user=user).get(id=classenrollment_id)
    except Enrollment.DoesNotExist:
        raise Exception('enrollment does not exist')
    
    if not class_enrollment.is_approved:
        return redirect('pending_approval')
    return class_enrollment