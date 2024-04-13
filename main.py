import os
from datetime import datetime
import argparse

DATA_DIRECTORY = ""
END_STRING = "--END--\n"

parser = argparse.ArgumentParser(
    prog="Markdown Diary",
    description="Keep a simple diary in md files.",
)

parser.add_argument(
    "--type",
    choices=["project", "diary"],
    default="project",
    help="""choose between a single md file (project) 
    or a directory with a file for every month""",
)
parser.add_argument(
    "--name",
    type=str,
    default="diary",
    help="""name for file if type is project 
    or name for directory if type is diary""",
)


def create_md_file(file_name: str, path: str = DATA_DIRECTORY) -> None:
    file_path = os.path.join(path, file_name)
    file_path += ".md"
    file = open(file_path, "w")
    file.close()


def on_init(args: argparse.Namespace) -> None:
    is_single = True if args.type == "project" else False
    if is_single:
        create_md_file(args.name)
    else:
        directory_contents = os.listdir()
        if args.name not in directory_contents:
            name = args.name if args.name else "diary"
            file_path = os.path.join(DATA_DIRECTORY, name)
            os.mkdir(file_path)


def add_date(file_path: str) -> None:
    today = datetime.today().strftime("%d/%m/%Y")
    file = open(file_path, "r+")
    content = file.read()
    file.seek(0)
    file.truncate()
    file.write(f"## {today}\n\n\n{content}")
    file.close()


def open_file(file_name: str) -> None:
    editor = os.environ.get("EDITOR", "nvim")
    add_date(file_name)
    os.system(f"{editor} +3 +'startinsert' {file_name}")


if __name__ == "__main__":
    args = parser.parse_args()
    directory_contents = os.listdir()
    directory_name = args.name
    file_name = args.name + ".md"
    if directory_name not in directory_contents and file_name not in directory_contents:
        on_init(args)
    open_file(file_name)
