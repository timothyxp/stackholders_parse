from bs4 import BeautifulSoup
from src.utils.logger import logger
from typing import List
import pandas as pd
from tqdm import tqdm
import bs4


def get_list_articles(page_file: str) -> List[str]:
    """
    :param page_file: downloaded html file from https://e-disclosure.ru/poisk-po-soobshheniyam
    :return: list of articles linked to this page
    """
    with open(page_file) as f:
        docs = f.read()

    page = BeautifulSoup(docs, "lxml")

    list_elem = page.find_all("div", {"id": "cont_wrap"})[0]
    elements = list_elem.find_all("td")
    logger.info(f"find {len(elements)} pages for parsing from {page_file}")

    articles = []

    for elem in elements:
        childrens = list(elem.children)
        if len(childrens) == 1:
            continue
        if len(childrens) != 7:
            logger.warning(f"can't parse elem with {len(childrens)=}")
            logger.debug(f"can't parse {elem=}")

        articles.append(childrens[3].attrs['href'])

    return articles


def parse_protocol_pages(pages_list: List[str], hrefs: List[str]) -> pd.DataFrame:
    texts_df = []
    errors = 0

    for i, page_file in enumerate(tqdm(pages_list)):
        try:
            with open(page_file, "r") as f:
                page = BeautifulSoup(f.read(), "lxml")

            texts = list(list(page.find_all("div", {"id": "cont_wrap"})[0].children)[3].children)
            texts = '\n'.join(text for text in texts if type(text) is bs4.element.NavigableString)

            texts_df.append([hrefs[i], texts])
        except:
            logger.debug(f"can't parse {page_file=}")
            errors += 1
            pass

    logger.info(f"have erro parse pages - {errors}, total parsed - {len(texts_df)}")
    texts_df = pd.DataFrame(texts_df, columns=["href", "text"])

    return texts_df
