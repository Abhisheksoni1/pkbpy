from django.core.management.base import BaseCommand
from apps.common.models import FinancialYear

class Command(BaseCommand):
    help = 'Create current financial year'

    def add_arguments(self, parser):
        parser.add_argument('finanacial_year', type=str, help='Current FY year')

    def handle(self, *args, **kwargs):
        current_financial_year= kwargs['finanacial_year']
        FinancialYear.objects.create(financial_year=current_financial_year)
        self.stdout.write("finanacial year added")

