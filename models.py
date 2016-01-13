from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ClockSession(models.Model):
	user = models.ForeignKey(User)

	in_time = models.DateTimeField(default = timezone.now)

	out_time = models.DateTimeField(null = True, blank = True)

	clocked_in = models.BooleanField(default = True)

	def clock_in(self):
		self.clocked_in = True
		self.save()

	def clock_out(self):
		self.out_time = timezone.now()
		self.clocked_in = False
		self.save()

	def __repr__(self):
		return '<' + str(self.user.first_name) + ', ' + str(self.in_time.date()) + '>'

	class Meta:
		get_latest_by = 'clocked_in'
		ordering = ['-in_time']
		verbose_name = 'Punchclock Session'
		verbose_name_plural = 'Punchclock Sessions'

