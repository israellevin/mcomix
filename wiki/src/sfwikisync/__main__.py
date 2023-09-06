#!/usr/bin/env python3

import argparse
import enum
import pathlib
import sys

from .wikiclient import WikiClient


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

    if args.operation == Operations.push.name and "bearertoken" not in args:
        parser.error(
            f"The {Operations.push.name} operation requires authentication with --bearertoken"
        )

    return args


def pull(client: WikiClient, contentdir: str) -> None:
    pagenames = client.pagenames()
    basedir = pathlib.Path(contentdir)
    for pagename in pagenames:
        page = client.page(pagename)
        page_path = basedir / page.filename()
        with open(page_path, "w") as fp:
            fp.write(page.text)


def main() -> int:
    program_args = parse_arguments()
    client = WikiClient(
        program_args.project, program_args.wikiname, program_args.bearertoken
    )

    import pdb; pdb.set_trace()
    if program_args.operation == Operations.pull.name:
        pull(client, program_args.contentdir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
