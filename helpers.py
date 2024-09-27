import logging
import yaml
from openai import OpenAI

# CONFIGURATION
# Charger la configuration depuis un fichier YAML
with open("config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# INITIALISATION DE L'API OPENAI
# Crée une instance du client OpenAI avec la clé API chargée depuis le fichier de configuration.
client_openai = OpenAI(
    api_key=config['openai'].get('apikey'),
)


# INITIALISATION DU LOGGER
class ColoredFormatter(logging.Formatter):
    # Codes de couleur ANSI pour les différents niveaux de log. 
    COLORS = {
        'DEBUG': '\033[94m',    # Bleu pour les messages de debug
        'INFO': '\033[92m',     # Vert pour les messages d'information
        'WARNING': '\033[93m',  # Jaune pour les avertissements
        'ERROR': '\033[91m',    # Rouge pour les erreurs
        'CRITICAL': '\033[95m', # Magenta pour les messages critiques
        'RESET': '\033[0m'      # Réinitialiser la couleur après le message
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']

        log_msg = super().format(record)
        return f"{log_color}{log_msg}{reset_color}"

# CONFIGURATION DE BASE DU LOGGER
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

# Appliquer le formatter coloré au handler de log
logger = logging.getLogger()
handler = logger.handlers[0]
handler.setFormatter(ColoredFormatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%dT%H:%M:%S'))


# EXPORTER LES HELPERS
__all__ = ['logger', 'config']