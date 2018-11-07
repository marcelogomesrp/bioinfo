from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import managers


class Enrollment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('account'))
    course_class = models.ForeignKey('courses.Class', verbose_name=_('class'),
                                        related_name='enrollment_set')
    date_added = models.DateTimeField(_('date added'), default=datetime.now)
    is_approved = models.BooleanField(default=False, db_column='approved')
    logged_in_time = models.IntegerField(default=0)
    
    # managers
    objects = models.Manager()
    approved = managers.ApprovedEnrollmentManager()
    pending = managers.PendingEnrollmentManager()
   
    class Meta:
        ordering = ('is_approved',)
        verbose_name, verbose_name_plural = _('enrollment'), _('enrollments')

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.course_class)
    
    def notify_user(self, template='enrollments/emails/approved.html'):
         from django.core.mail import EmailMessage
         from django.template import Context, loader
         t = loader.get_template(template)
         text = t.render(Context({'enrollment': self}))
         msg = EmailMessage(_('%s: Your enrollment has been approved' % self.course_class.code.upper()), 
                            text, 
                            settings.FROM_EMAIL, [self.user.email])
         msg.send()