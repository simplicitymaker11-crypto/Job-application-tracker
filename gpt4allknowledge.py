from pathlib import Path

# ------------------------------------------
# PATHS
# ------------------------------------------

SOURCE = Path(r"D:/gpt4all-knowledge")

OUTPUT = Path(r"D:/GPT4All_Combined")

OUTPUT.mkdir(parents=True, exist_ok=True)


# ------------------------------------------
# SETTINGS
# ------------------------------------------

# Maximum size of each combined TXT file.
# 5 MB keeps files reasonably manageable.
MAX_SIZE = 5 * 1024 * 1024

TEXT_EXTENSIONS = {
    ".md",
    ".rst",
    ".txt",
    ".html",
    ".htm"
}


def clean_name(name):
    """Make folder name safe for output filename."""

    return (
        name.replace(" ", "_")
            .replace(".", "_")
            .replace("-", "_")
    )


def combine_folder(folder):

    print(f"\nProcessing: {folder.name}")

    files = []

    for file in folder.rglob("*"):

        if (
            file.is_file()
            and file.suffix.lower() in TEXT_EXTENSIONS
        ):
            files.append(file)

    if not files:
        print("No text documents found.")
        return

    print(f"Found {len(files)} documents")

    part = 1
    current_size = 0

    output_name = clean_name(folder.name)

    output_file = OUTPUT / f"{output_name}_part_{part}.txt"

    writer = open(
        output_file,
        "w",
        encoding="utf-8",
        errors="ignore"
    )

    for number, file in enumerate(files, start=1):

        try:

            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            # Preserve where the information came from
            header = f"""

============================================================
SOURCE FILE: {file.relative_to(SOURCE)}
============================================================

"""

            content = header + text + "\n\n"

            content_size = len(
                content.encode("utf-8")
            )

            # Start another part if current file becomes too large
            if (
                current_size + content_size > MAX_SIZE
                and current_size > 0
            ):

                writer.close()

                part += 1
                current_size = 0

                output_file = OUTPUT / (
                    f"{output_name}_part_{part}.txt"
                )

                writer = open(
                    output_file,
                    "w",
                    encoding="utf-8",
                    errors="ignore"
                )

            writer.write(content)

            current_size += content_size

            if number % 100 == 0:
                print(
                    f"  Combined {number}/{len(files)}"
                )

        except Exception as error:

            print(f"Skipped: {file}")
            print(f"Reason: {error}")

    writer.close()

    print(
        f"Finished {folder.name} "
        f"→ {part} combined file(s)"
    )


def main():

    print("GPT4All Documentation Combiner")
    print("=" * 40)

    # Each top-level folder becomes its own collection
    folders = [
        folder
        for folder in SOURCE.iterdir()
        if folder.is_dir()
    ]

    print(f"Found {len(folders)} main folders.")

    for folder in folders:
        combine_folder(folder)

    print("\n" + "=" * 40)
    print("FINISHED")
    print("=" * 40)

    print(f"\nCombined files saved in:\n{OUTPUT}")


if __name__ == "__main__":
    main()