import requests
import re
from config import Config
from pathlib import Path
from tqdm import tqdm
from loguru import logger


def fetch_json(url):
    logger.debug("fetch domains list...")
    r = requests.get(url)
    assert r.status_code == 200
    return r.json()
    

def make_filter_list(domains, skiplist, skipsubs):
    logger.debug("make filter list...")

    filtered_domains = [None for _ in range(len(domains))]
    
    chars = re.compile(r"\w+")
    dig_or_word = re.compile(r"[a-zA-Z]+|\d+")

    for i , domain in tqdm(list(enumerate(domains))):
        domain = str(domains[i])

        skip = False
        for subs in skipsubs:
            if subs in domain:
                filtered_domains[i] = False
                skip = True
                break
        if skip:
            continue

        subd = set(re.findall(dig_or_word, domain)) | set(re.findall(chars, domain))
    
        for subs in skiplist:
            if subs in subd:
                filtered_domains[i] = False
                skip = True
                break
        if skip:
            continue

        filtered_domains[i] = True

    return filtered_domains


def remove_prefixes(domains, prefixes):
    logger.debug("remove prefixes...")
    wo_prefix_ls = []
    for domain in tqdm(domains):
        for prefix in prefixes:
            if domain.startswith(prefix):
                domain = domain[len(prefix):]
        wo_prefix_ls.append(domain)
    return wo_prefix_ls


def run():
    if Path(Config.DOMAINS_PATH).exists():
        with open(Path(Config.DOMAINS_PATH)) as f:
            logger.debug(f"{Path(Config.DOMAINS_PATH)} exists, read...")
            domains = f.read().split()
    else:
        domains = fetch_json(Config.DOMAIN_URL_JSON)

    with open(Path(Config.PREFIXES_PATH)) as f:
        prefixes = f.read().split()
        
    domains_wo_prefix = remove_prefixes(domains, prefixes)
    with open(Path(Config.DOMAINS_WO_PREFIX_PATH), "w") as f:
        f.writelines((f"{domain}\n" for domain in domains_wo_prefix))

    with open(Path(Config.SKIPLIST_PATH)) as skiplist_f, \
         open(Path(Config.SKIPSUBS_PATH)) as skipsubs_f, \
         open(Path(Config.FILTER_LIST_PATH), "w") as filter_f:

        skiplist = skiplist_f.read().split()
        skipsubs = skipsubs_f.read().split()

        mask = make_filter_list(
            domains=domains_wo_prefix, 
            skiplist=skiplist,
            skipsubs=skipsubs,
        )

        filter_f.writelines((f"{b}\n" for b in mask))

    with open(Path(Config.DOMAINS_FILTERED_PATH), "w") as f:
        f.writelines((f"{domain}\n" for i, domain in enumerate(domains_wo_prefix) if bool(mask[i])))

if __name__ == "__main__":
    run()
