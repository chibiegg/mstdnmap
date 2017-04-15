import logging
import traceback
from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError

from mstdnmap.mstdn.models import Instance

logger = logging.getLogger(__name__)


def get_connected_hostname(instance):
    try:
        timeline = instance.get_timeline()
    except KeyboardInterrupt:
        raise
    except:
        logger.warn("Cannot get timeline: %s", instance.hostname)
        return []

    logger.warn("get %s", instance.hostname)

    instance_hostnames = set()

    for t in timeline:
        account = t["account"]["acct"]
        if not "@" in account:
            continue

        hostname = account.split("@")[1]
        instance_hostnames.add(hostname)

    return list(instance_hostnames)


def update_connections(instance, connected_hostnames):
    created_instances = []
    instances = []
    for hostname in connected_hostnames:
        target_instance, created = Instance.objects.get_or_create(hostname=hostname)
        instances.append(target_instance)
        if created:
            created_instances.append(target_instance)

    instance.connections.add(*instances)
    instance.save()
    return created_instances


def handle_instance(instance):
    return update_connections(instance, get_connected_hostname(instance))


def pool_func(instance):
    return (instance, get_connected_hostname(instance))


class Command(BaseCommand):

    def handle(self, *args, **options):
        created_instances = []

        pool = Pool(50)
        for i in pool.map(pool_func, Instance.objects.all()):
            created_instances += update_connections(i[0], i[1])

        while True:
            created_instances = []
            instances = created_instances[:]
            for i in pool.map(pool_func, instances):
                created_instances += update_connections(i[0], i[1])

            if len(created_instances) == 0:
                break
