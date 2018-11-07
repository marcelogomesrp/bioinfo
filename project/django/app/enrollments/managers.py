# coding: utf-8
from datetime import datetime
from django.db import models


class ApprovedEnrollmentManager(models.Manager):
    def get_query_set(self):
        return super(ApprovedEnrollmentManager, self).get_query_set().\
                    filter(is_approved=True)


class PendingEnrollmentManager(models.Manager):
    def get_query_set(self):
        return super(PendingEnrollmentManager, self).get_query_set().\
                    filter(is_approved=False)