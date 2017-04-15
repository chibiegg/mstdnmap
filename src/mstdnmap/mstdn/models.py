from django.db import models


class Instance(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "Instance"

    hostname = models.CharField("Hostname", max_length=1024)
    connections = models.ManyToManyField("self", related_name='reverse_connections', blank=True)

    def __str__(self):
        return self.hostname
