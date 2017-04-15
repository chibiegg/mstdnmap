import logging
import traceback
from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError

from mstdnmap.mstdn.models import Instance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<hostname>'

    def add_arguments(self, parser):
        parser.add_argument('hostname', type=str)

    def handle(self, *args, **options):
        hostname = options["hostname"]
        logger.info('hostname: %s' % hostname)

        try:
            instance = Instance.objects.get(hostname=hostname)
            logger.error("already exists")
        except Instance.DoesNotExist:
            instance = Instance(hostname=hostname)
            instance.get_timeline()
            instance.save()
