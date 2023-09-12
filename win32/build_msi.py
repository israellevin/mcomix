#!/usr/bin/env python3

import enum
import os
import pathlib
import re
import shutil
import subprocess
import sys

# Patch import path to be able to import the mcomix module
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from mcomix.constants import VERSION

INDENT_ONELEVEL = "  "

MAX_ID_LENGTH = 72


class IdType(enum.Enum):
    Directory = 1
    Component = 2
    File = 3


def normalize_mcomix_version() -> str:
    """WiX doesn't like any suffixes appended to the version, so only take the
    usual version triplet."""
    match = re.match(r"^(\d+\.\d+\.\d+)", VERSION)
    if match:
        return match.group(1)
    else:
        raise AttributeError()


def shorten_dir_part(text: str, length: int) -> str:
    """Makes sure the passed text is no longer than <length>,
    equally distributing the available length to the front of the
    text and the end of the text."""
    if len(text) <= length:
        return text
    half_len = length // 2
    return text[:half_len] + text[-half_len:]


def generate_id_suffix(idtype: IdType) -> str:
    """Generates an ID suffix based on ID type."""
    if idtype == IdType.Directory:
        return ".d"
    elif idtype == IdType.Component:
        return ".c"
    elif idtype == IdType.File:
        return ".f"

    return ".unknown"


def generate_id_from_string(
    path: pathlib.PurePath, root: pathlib.PurePath, idtype: IdType
) -> str:
    """Transforms the text in such a way that it conforms to ID requirements, i.e.
    certain chars must be absent, max. 72 characters, starting with character or underscore.
    """
    suffix = generate_id_suffix(idtype)
    if path != root:
        relative_path = path.relative_to(root)
        # Take the first letter from all path parts, exclude the filename
        pathparts = [shorten_dir_part(part, 4) for part in relative_path.parts[:-1]]
        dirpart_length = sum(len(part) for part in pathparts) + len(
            pathparts
        )  # Assuming a single char separator between each part
        avail_remaining_length = MAX_ID_LENGTH - dirpart_length - len(suffix)
        # Take the full filename
        pathparts.append(relative_path.name[-avail_remaining_length:])
    else:
        # Since MComix.d is hardcoded as dir id further down, this special handling makes sure the same ID
        # is generated here for the root directory
        pathparts = [path.name]

    safetext = re.sub(r"[-/\\@+]", "_", "_".join(pathparts))

    if not safetext[0].isalpha():
        safetext = "_" + safetext

    return safetext + suffix


def generate_xml_entries_for_path(
    dirs_xml: list[str],
    components_xml: list[str],
    compgroup_xml: list[str],
    current_directory: pathlib.Path,
    root_dir: pathlib.PurePath,
    depth: int,
) -> None:
    """Generates various XML elements by descending into the root directory
    and gathering files and directories. The function fills the _xml lists."""
    indent = INDENT_ONELEVEL * depth

    # First, iterate over all directories, possibly calling this function recursively,
    # to generate the output directory structure.
    for path in current_directory.iterdir():
        if path.is_dir():
            path_id = generate_id_from_string(path, root_dir, IdType.Directory)

            dirs_xml.append(f"{indent}<Directory Id='{path_id}' Name='{path.stem}'>")
            xml_entries = len(dirs_xml)
            generate_xml_entries_for_path(
                dirs_xml, components_xml, compgroup_xml, path, root_dir, depth + 1
            )

            # If no new directories were added, shorten last directory tag
            if len(dirs_xml) == xml_entries:
                dirs_xml[-1] = dirs_xml[-1].replace(">", "/>")
            else:
                dirs_xml.append(f"{indent}</Directory>")

    # Since this function is called once for each directory, also collect all files
    # in the current directory, and create Component pairs for the files.
    current_component_index = len(components_xml)
    files_in_dir = False
    for path in current_directory.iterdir():
        if path.is_file():
            files_in_dir = True
            component_id = generate_id_from_string(path, root_dir, IdType.Component)
            file_id = generate_id_from_string(path, root_dir, IdType.File)
            components_xml.append(f"{INDENT_ONELEVEL}<Component Id='{component_id}'>")
            components_xml.append(
                f"{INDENT_ONELEVEL*2}<File Id='{file_id}' Name='{path.name}' KeyPath='yes' />"
            )
            components_xml.append(f"{INDENT_ONELEVEL}</Component>")

            # For the ComponentGroup element, collect all component references generated above
            compgroup_xml.append(
                f"{INDENT_ONELEVEL}<ComponentRef Id='{component_id}' />"
            )

    # If files were found in the directory, insert a DirectoryRef element around the created components.
    if files_in_dir:
        current_directory_id = generate_id_from_string(
            current_directory, root_dir, IdType.Directory
        )
        absolute_current_dir = pathlib.Path.cwd() / current_directory
        relative_current_dir = absolute_current_dir.relative_to(pathlib.Path.cwd())
        components_xml.insert(
            current_component_index,
            f"<DirectoryRef Id='{current_directory_id}' FileSource='{relative_current_dir}'>",
        )
        components_xml.append("</DirectoryRef>")


def generate_wix_fileset(releasedir: pathlib.Path) -> str:
    """Create the WiX fragment XML content that contains all files in a single
    ComponentGroup called APPLICATIONFILES."""
    dirs_xml: list[str] = []
    components_xml: list[str] = []
    compgroup_xml: list[str] = []

    generate_xml_entries_for_path(
        dirs_xml, components_xml, compgroup_xml, releasedir, releasedir, 0
    )

    dirs_xml = (
        [
            "<Directory Id='TARGETDIR' Name='SourceDir'>",
            "<Directory Id='ProgramFiles64Folder'>",
            f"<Directory Id='MComix{generate_id_suffix(IdType.Directory)}' Name='MComix'>",
        ]
        + dirs_xml
        + ["</Directory>", "</Directory>", "</Directory>"]
    )

    compgroup_xml = (
        ["<ComponentGroup Id='APPLICATIONFILES'>"]
        + compgroup_xml
        + ["</ComponentGroup>"]
    )

    dirs = "\n".join(dirs_xml)
    components = "\n".join(components_xml)
    compgroups = "\n".join(compgroup_xml)

    final_xml = f"""<?xml version='1.0' encoding='utf-8'?>
<Wix xmlns='http://schemas.microsoft.com/wix/2006/wi'>
<Fragment>
{dirs}

{components}

{compgroups}
</Fragment>
</Wix>
"""
    return final_xml


def compile_msi(
    input_files: list[pathlib.PurePath],
    temp_dir: pathlib.PurePath,
    output_dir: pathlib.PurePath,
) -> None:
    """Run WiX v3 tooling to compile and link the input files into a MSI file placed
    in the output directory."""
    candle = shutil.which("candle.exe")
    light = shutil.which("light.exe")
    if not candle or not light:
        print(
            "Error: Could not find WiX toolset candle/light executables on PATH",
            file=sys.stderr,
        )
        sys.exit(1)

    # Compile WXS files
    cmd = (
        [candle]
        + [str(path) for path in input_files]
        + [
            f"-dVERSION={normalize_mcomix_version()}",
            "-arch",
            "x64",
            "-o",
            str(temp_dir) + os.sep,
        ]
    )
    subprocess.run(cmd, check=True)

    # Link generated output files
    msi_path = output_dir.joinpath(f"mcomix-win64-{VERSION}.msi")
    cmd = (
        [light]
        + [
            str(temp_dir.joinpath(path.name).with_suffix(".wixobj"))
            for path in input_files
        ]
        + ["-o", str(msi_path), "-spdb"]
    )
    subprocess.run(cmd, check=True)


def main() -> None:
    spec = pathlib.Path("win32/mcomix.wxs")
    win32_builddir = pathlib.Path("dist/MComix")
    if not spec.exists() or not win32_builddir.exists():
        print(
            "Error: WiX specification or release directory do not exist, "
            "make sure you are in the correct working directory.",
            file=sys.stderr,
        )
        return

    tmpdir = pathlib.Path("build/")
    if not tmpdir.is_dir():
        tmpdir.mkdir()

    # Generate file list and create auxilary WXS file
    autogen_filename = tmpdir.joinpath(f"mcomix-frag-{VERSION}.wxs")
    with open(autogen_filename, "w") as fp:
        autogen_fragment_wix_content = generate_wix_fileset(win32_builddir)
        fp.write(autogen_fragment_wix_content)

    # Generate MSI
    compile_msi(
        [pathlib.PurePath("win32/mcomix.wxs"), autogen_filename],
        tmpdir,
        pathlib.PurePath("dist/"),
    )


if __name__ == "__main__":
    main()
