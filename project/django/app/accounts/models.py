# coding: utf-8
import md5
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from util.custom_fields import UUIDField


class UserProfile(models.Model):
	""" User profile class linked to the User class (from django.contrib.auth) """
	user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
	birth_date = models.DateField(_('birth date'))
	institution_name = models.CharField(_('institution'), max_length=64)
	institution_city = models.CharField(_('city'), max_length=64)
	institution_state = models.CharField(_('state'), max_length=2)
	course = models.CharField(_('course'), max_length=64)
	enrollment_year = models.CharField(_('enrollment year'), max_length=4)
	last_update = models.DateTimeField(_('last update'), default=datetime.now)
	logged_in_time = models.IntegerField(default=0)

	class Meta:
		ordering = ['user']
		verbose_name, verbose_name_plural = _('account'), _('accounts')

	def __unicode__(self):
		return self.user.get_full_name()
	
	def save(self, *args, **kwargs):
		if self.id:
			last_update = datetime.now()
		super(UserProfile, self).save(*args, **kwargs)
	
	def get_logged_in_time_hash(self):
		''' Gera uma chave para que o usuário não tente marcar mais tempo '''
		m = md5.new()
		m.update(str(self.logged_in_time))
		return m.hexdigest()

	@models.permalink
	def get_absolute_url(self):
		return ('view_account', [self.uuid])