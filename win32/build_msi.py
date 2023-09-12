#!/usr/bin/env python3

import pathlib
import re
import sys

INDENT_ONELEVEL = "  "


def escape_path_for_id(text: str) -> str:
    return re.sub(r"[-/\\]", "_", text)


def generate_xml_entries_for_path(
    dirs_xml: list[str],
    current_directory: pathlib.Path,
    root_dir: pathlib.PurePath,
    depth: int,
) -> None:
    indent = INDENT_ONELEVEL * depth
    for path in current_directory.iterdir():
        fullpath = path.relative_to(root_dir)
        current_path_id = (
            escape_path_for_id(str(fullpath)) + ".dir" if path.is_dir() else ""
        )

        if path.is_dir() and path.stem != "__pycache__":
            dirs_xml.append(
                f"{indent}<Directory Id='{current_path_id}' Name='{path.stem}'>"
            )
            xml_entries = len(dirs_xml)
            generate_xml_entries_for_path(dirs_xml, path, root_dir, depth + 1)

            # If no new directories were added, shorten last directory tag
            if len(dirs_xml) == xml_entries:
                dirs_xml[-1] = dirs_xml[-1].replace(">", "/>")
            else:
                dirs_xml.append(f"{indent}</Directory>")


def generate_wix_fileset(releasedir: pathlib.Path) -> str:
    dir_id_ext = ".dir"
    dirs_xml: list[str] = []
    generate_xml_entries_for_path(dirs_xml, releasedir, releasedir, 0)

    dirs_xml = (
        [
            "<Directory Id='TARGETDIR' Name='SourceDir'>",
            "<Directory Id='ProgramFiles64Folder'>",
            f"<Directory Id='MComix{dir_id_ext}' Name='MComix'>",
        ]
        + dirs_xml
        + ["</Directory>", "</Directory>", "</Directory>"]
    )

    return "\n".join(dirs_xml)


def main() -> None:
    spec = pathlib.Path("win32/mcomix.wxs")
    # releasedir = pathlib.Path('dist/MComix') FIXME: This is the real path
    releasedir = pathlib.Path("mcomix")
    if not spec.exists() or not releasedir.exists():
        print(
            "Error: WiX specification or release directory do not exist, "
            "make sure you are in the correct working directory.",
            file=sys.stderr,
        )
        return

    print(generate_wix_fileset(releasedir))


if __name__ == "__main__":
    main()
