from django.core.management.base import BaseCommand
from optparse import make_option
from api import seeds
from api.v1.users.models import User
import sys


def model_import(name):
    __import__(name)
    return sys.modules[name]


class SeedException(Exception):
    pass


class Command(BaseCommand):
    MODEL_LIST_WITH_ORDER = [
        'user', 'flog', 'flatgram'
    ]

    help = 'Seed your Django database with fake data'
    args = "[modelname ...]"

    option_list = [
        make_option('--number', dest='number', default=40,
                    help='number of each model to seed'),
    ]

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('model', nargs='?', type=str, help='model name',
                            default=None, const=False)
        parser.add_argument('--number', nargs='?', type=int, default=40,
                            const=40, help='number of each model to seed')

    def handle(self, *args, **options):
        model_name = options['model']
        try:
            number = int(options['number'])
        except ValueError:
            raise SeedException('The value of --number must be an integer')

        if model_name is None:
            for i in self.MODEL_LIST_WITH_ORDER:
                mod = model_import("api.seeds.%s" % i)
                mod.generate_data(number)
            self.stdout.write(self.style.SUCCESS('Done'))
            return
        try:
            mod = model_import("api.seeds.%s" % model_name)
            mod.generate_data(number)
            self.stdout.write(self.style.SUCCESS('done'))
        except ModuleNotFoundError:
            self.stdout.write(
                self.style.ERROR('%s model is not found' % model_name))

