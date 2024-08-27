import subprocess
import pathlib
import sys

from invoke import task

KNOWN_WORDS = ["aspell", "tex", "en_GB"]


def get_files_to_check():
    for path in pathlib.Path("cv/").glob("*.tex"):
        yield path


@task
def spellcheck(c):
    exit_code = 0

    for tex_path in get_files_to_check():

        tex = tex_path.read_text()
        aspell_output = subprocess.check_output(
            ["aspell", "-t", "--list", "--lang=en_GB"], input=tex, text=True
        )
        incorrect_words = set(aspell_output.split("\n")) - {""} - KNOWN_WORDS
        if len(incorrect_words) > 0:
            print(f"In {tex_path} the following words are not known: ")
            for string in sorted(incorrect_words):
                print(string)
            exit_code = 1

    sys.exit(exit_code)
