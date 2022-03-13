import asyncio
from pathlib import Path
from tqdm import tqdm
from config import Config
from loguru import logger


async def check_domain(domain):
    proc = await asyncio.create_subprocess_exec(
        "curl",  
        *['-4', '-I', '-m', '5', domain], 
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode


async def check_chunk(domains, request_limit):
    semaphore = asyncio.Semaphore(request_limit)
    async with semaphore:
        res = await asyncio.gather(*(check_domain(domain) for domain in domains))
    return res


def filter_domains(domains, codes):
    return [domain for i, domain in enumerate(domains) if int(codes[i]) == 0]


def chunks(ls, size):
    for chunk_start in tqdm(range(0, len(ls), size)):
        chunk_end = chunk_start + size
        yield ls[chunk_start:chunk_end]


def check_domains(domains, chunk_size, request_limit):
    codes = []
    for chunk in chunks(domains, chunk_size):
        codes_chunk = asyncio.run(check_chunk(chunk, request_limit=request_limit))
        codes += codes_chunk
    return codes


def run():
    logger.debug("check available...")
    with open(Path(Config.DOMAINS_FILTERED_PATH)) as f:
        domains = f.read().split()

    done_previously = 0
    available_mask_path = Path(Config.AVAILABLE_MASK_PATH)
    if available_mask_path.exists():
        with open(available_mask_path) as f:
            done_previously = len(f.readlines())
        logger.info(f"{available_mask_path} exisis. already done: {done_previously}")

    for chunk in chunks(domains[done_previously:], Config.CHUNK_SIZE):
        codes = asyncio.run(check_chunk(chunk, request_limit=Config.REQUEST_LIMIT))

        available_domains = filter_domains(chunk, codes)
        
        with open(Path(Config.AVAILABLE_DOMAINS_PATH), "a") as av_domains_f, \
             open(Path(Config.AVAILABLE_MASK_PATH), "a") as mask_path_f:
            av_domains_f.writelines((f"{domain}\n" for i, domain in enumerate(available_domains) if codes[i] == 0))
            mask_path_f.writelines((f"{code}\n" for code in codes))
    

if __name__ == "__main__":
    run()