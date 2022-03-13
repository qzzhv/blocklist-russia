import domain_list
import check_available
from pathlib import Path
from config import Config


if not Path(Config.DOMAINS_FILTERED_PATH).exists():
    domain_list.run()

check_available.run()