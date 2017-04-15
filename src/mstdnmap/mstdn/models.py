from django.db import models

import requests


class Instance(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "Instance"

    hostname = models.CharField("Hostname", max_length=1024, unique=True)
    connections = models.ManyToManyField("self", related_name='reverse_connections', blank=True)

    def __str__(self):
        return self.hostname

    def get_timeline(self):
        url = "https://{0}/api/v1/timelines/public".format(self.hostname)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
