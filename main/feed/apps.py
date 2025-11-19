import os
from django.apps import AppConfig
from django.core.management import call_command

class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        # Só executa automaticamente no ambiente do Render
        if os.environ.get("RENDER"):
            try:
                call_command("deploy_setup")
            except Exception as e:
                print(f"Erro ao rodar deploy_setup automaticamente: {e}")
