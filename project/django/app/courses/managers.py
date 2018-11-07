# coding: utf-8
from datetime import datetime
from django.db import models


class ActiveClassManager(models.Manager):
    def get_query_set(self):
        return super(ActiveClassManager, self).get_query_set().\
                    filter(start_date__lte=datetime.now(), end_date__gte=datetime.now())