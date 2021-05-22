import argparse
from src.utils.logger import logger
from config import config
from src.parse.html import get_list_articles, parse_protocol_pages
from src.downloader import download_list_pages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("parse_list", help="html file from e-disclosure.ru for parse pages")
    parser.add_argument("-t", "--test", action="store_true", help="for prevent ddos blocking test in test mode")
    parser.add_argument("--ignore_cache", action="store_true",
                        help="if you want ignore cache, also you can delete cache directory")

    args = parser.parse_args()

    pages_list = get_list_articles(args.parse_list)

    downloaded_pages_list = download_list_pages(
        pages_list,
        config.pages_cache_dir,
        args.test,
        not args.ignore_cache
    )

    result_df = parse_protocol_pages(downloaded_pages_list, pages_list)

    logger.info(f"write results to {config.parsed_data_file}")
    result_df.to_parquet(config.parsed_data_file)


if __name__ == "__main__":
    main()
