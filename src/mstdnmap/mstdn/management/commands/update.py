import logging
import traceback
from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError

from mstdnmap.mstdn.models import Instance

logger = logging.getLogger(__name__)


def handle_instance(instance):
    try:
        timeline = instance.get_timeline()
    except KeyboardInterrupt:
        raise
    except:
        logger.warn("Cannot get timeline: %s", instance.hostname)
        return []

    logger.warn("%s", instance.hostname)

    instance_hostnames = set()

    for t in timeline:
        account = t["account"]["acct"]
        if not "@" in account:
            continue

        hostname = account.split("@")[1]
        instance_hostnames.add(hostname)

    instance_hostnames = list(instance_hostnames)

    created_instances = []
    instances = []
    for hostname in instance_hostnames:
        target_instance, created = Instance.objects.get_or_create(hostname=hostname)
        instances.append(target_instance)
        if created:
            created_instances.append(target_instance)

    instance.connections.add(*instances)
    instance.save()

    return created_instances


class Command(BaseCommand):

    def handle(self, *args, **options):
        created_instances = []
        for instance in Instance.objects.all():
            created_instances += handle_instance(instance)

        while True:
            created_instances = []
            instances = created_instances[:]
            for instance in instances:
                created_instances += handle_instance(instance)

            if len(created_instances) == 0:
                break
