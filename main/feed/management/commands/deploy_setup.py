from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Executa migrações e carrega dados iniciais automaticamente no deploy"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Executando migrações..."))
        call_command("makemigrations", "feed")
        call_command("migrate")

        self.stdout.write(self.style.WARNING("Carregando dados iniciais..."))
        try:
            call_command("loaddata", "categories.json")
            call_command("loaddata", "articles.json")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao carregar dados: {e}"))

        self.stdout.write(self.style.SUCCESS("Setup de deploy finalizado!"))
