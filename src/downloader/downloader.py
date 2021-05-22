from typing import List
import requests
from tqdm import tqdm
import os
from src.utils.logger import logger


def download_list_pages(
        pages_list: List[str],
        cache_dir: str,
        test: bool = False,
        use_cache: bool = True,
        verbose=True
) -> List[str]:
    """
    implement simple download, for production should link VPN
    :param pages_list: list of pages to download
    :param cache_dir: directory where we will store pages
    :param test: for prevent ddos blocking will parse only one page
    :param use_cache: use cache pages or not
    :return: list of files where pages stored
    :param verbose:
    """
    if test:
        pages_list = pages_list[:1]

    parsed_pages = []

    try:
        pages_iter = enumerate(pages_list)
        if verbose:
            pages_iter = tqdm(pages_iter, total=len(pages_list))

        for i, article in pages_iter:
            page_name = article.split('?')[1]
            page_path = os.path.join(cache_dir, page_name)

            if use_cache and os.path.exists(page_path):
                continue

            with open(page_path, "w") as f:
                f.write(requests.get(article).content.decode("utf-8"))

            parsed_pages.append(page_path)

    except ConnectionRefusedError:
        logger.warning(f"ddos block, cannot parse more, change IP, total_parse={i} pages, continue running")

    finally:
        logger.info(f"download {len(parsed_pages)} pages")
        return parsed_pages
