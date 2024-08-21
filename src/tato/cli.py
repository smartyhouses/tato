import argparse
import sys
from pathlib import Path

import libcst.tool
from libcst._version import __version__ as libcst_version
from libcst.helpers import paths

from tato.__about__ import __version__
from tato.index.index import Index


def main() -> None:
    parser = argparse.ArgumentParser(description="Tato CLI tool")
    parser.add_argument(
        "--version",
        action="version",
        version=f"tato version {__version__} (libcst version {libcst_version})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Index subcommand
    index_parser = subparsers.add_parser("index", help="Create an index")
    index_parser.add_argument("path", help="Package to index")

    # Codemod subcommand
    format_parser = subparsers.add_parser("format", help="Run format command")
    format_parser.add_argument("paths", nargs="+", help="Paths to process")
    format_parser.add_argument("--with-index", help="Path to index file")

    args = parser.parse_args()

    if args.command == "index":
        # chdir so the fully_qualified_name of the module matches Python's
        p = Path(args.path)
        with paths.chdir(p.parent):
            index_path = Path(p.name).joinpath("tato-index.sqlite3")
            index_path.unlink(missing_ok=True)
            Index(index_path).create()
        sys.exit(0)
    elif args.command == "format":
        # The help text from libcst spits out 'usage: tato codemod' and exposes the
        # underlying libcst configuration. We can reuse that for now.
        libcst_args = ["codemod", "-x", "tato.tato.ReorderFileCodemod"]
        if args.with_index:
            libcst_args.extend(["--with-index", args.with_index])
        sys.exit(libcst.tool.main("tato", libcst_args + args.paths))
