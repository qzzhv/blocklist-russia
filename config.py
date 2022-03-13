class Config:

    ###  domain_list
    DOMAIN_URL_JSON = r"https://reestr.rublacklist.net/api/v2/domains/json/"
    FILTER_LIST_PATH = r"output/filter_mask.txt"
    AVAILABLE_MASK_PATH = r"output/available_mask.txt"
    DOMAINS_PATH = r"output/domains.txt"
    DOMAINS_WO_PREFIX_PATH = r"output/domains_wo_prefix.txt"
    DOMAINS_FILTERED_PATH = "output/domains_filtered.txt"
    
    SKIPLIST_PATH = r"skiplist.txt"
    SKIPSUBS_PATH = r"skipsubs.txt"
    PREFIXES_PATH = r"prefixes.txt"

    ###  check_available
    AVAILABLE_DOMAINS_PATH = "output/domains_available.txt"
    REQUEST_LIMIT = 15
    CHUNK_SIZE = 1000
