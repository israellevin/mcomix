#!/usr/bin/env python3

import argparse
import enum
import glob
import logging
import pathlib
import sys

from .wikiclient import WikiClient
from .wikipage import WikiPage


class Operations(enum.Enum):
    pull = 0
    push = 1


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=pathlib.Path(sys.argv[0]).name,
        description="Synchronize a folder of Markdown documents with an Allura wiki hosted by SourceForge",
    )
    parser.add_argument("-p", "--project", required=True)
    parser.add_argument("-w", "--wikiname", default="wiki")
    parser.add_argument("-d", "--contentdir", default="content")
    parser.add_argument("-b", "--bearertoken")
    parser.add_argument(
        "operation", choices=[enumvalue.name for enumvalue in Operations]
    )
    args = parser.parse_args()

    if args.operation == Operations.push.name and not args.bearertoken:
        parser.error(
            f"The {Operations.push.name} operation requires authentication with --bearertoken"
        )

    return args


def pull(client: WikiClient, contentdir: str) -> None:
    """Read the contents of all wiki pages, and write them into the content directory.
    Existing files are overwritten without confirmation."""
    logging.info("Retrieving list of Wiki pages")
    pagenames = client.pagenames()
    basedir = pathlib.Path(contentdir)
    for pagename in pagenames:
        page = client.page(pagename)
        if not page:
            logging.error(f"Page '{pagename}' could not be downloaded")
            continue
        else:
            logging.info(f"Downloaded '{pagename}'")

        page_path = basedir / page.filename()
        with open(page_path, "w") as fp:
            fp.write(page.text)


def read_page_text(path: pathlib.Path) -> str:
    """Reads the content of the given path, converting line endings to Windows endings if needed (since
    the SF API seems to store page text with Windows line endings."""
    with open(path, "r") as fp:
        page_text = fp.read()
        if "\r\n" not in page_text and "\n" in page_text:
            page_text = page_text.replace("\n", "\r\n")
        return page_text


def push(client: WikiClient, contentdir: str) -> None:
    """Reads all markdown files from the content directory, and creates matching wiki pages for them.
    Update is only performed if the pages differ."""
    for filename in glob.glob(f"{contentdir}/*.md"):
        path = pathlib.Path(filename)
        page_title = path.stem
        page_text = read_page_text(path)

        # Copy labels from old page if they exist, since the script has no way to store labels at the moment
        old_page = client.page(page_title)
        labels = old_page.labels if old_page else []
        new_page = WikiPage(title=page_title, text=page_text, labels=labels)

        if not old_page or old_page.text != new_page.text:
            client.create_or_update_page(new_page)
            logging.info(f"Updated '{page_title}'")
        else:
            logging.info(f"No change to '{page_title}'")


def main() -> int:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
    program_args = parse_arguments()
    client = WikiClient(
        program_args.project, program_args.wikiname, program_args.bearertoken
    )

    if program_args.operation == Operations.pull.name:
        pull(client, program_args.contentdir)
    elif program_args.operation == Operations.push.name:
        push(client, program_args.contentdir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
