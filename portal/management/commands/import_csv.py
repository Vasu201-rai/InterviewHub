from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from portal.admin import QuestionResource
import tablib


class Command(BaseCommand):
    help = "Import questions from a CSV file directly into the database (bypasses admin/WAF)."

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        try:
            with open(csv_path, 'rb') as f:
                data = tablib.Dataset().load(f.read().decode('utf-8-sig'), format='csv')
        except FileNotFoundError:
            raise CommandError(f"File not found: {csv_path}")

        if not User.objects.filter(is_superuser=True).exists():
            raise CommandError("No superuser found. Create one first with createsuperuser.")

        resource = QuestionResource()
        result = resource.import_data(data, dry_run=True, raise_errors=False)

        if result.has_errors() or result.has_validation_errors():
            self.stdout.write(self.style.ERROR("Errors found during dry run:"))
            for row_error in result.row_errors():
                row_num, errors = row_error
                for error in errors:
                    self.stdout.write(self.style.ERROR(f"Row {row_num}: {error.error}"))
            for invalid_row in result.invalid_rows:
                self.stdout.write(self.style.ERROR(f"Row {invalid_row.number}: {invalid_row.error_dict}"))
            self.stdout.write(self.style.WARNING("Dry run had errors. Nothing was imported. Fix the CSV and try again."))
            return

        # Real import
        result = resource.import_data(data, dry_run=False, raise_errors=True)
        self.stdout.write(self.style.SUCCESS(
            f"Import complete: {result.totals['new']} new, {result.totals['update']} updated, {result.totals['skip']} skipped."
        ))