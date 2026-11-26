#!/usr/bin/env python3
"""Last Text at One Percent — make.fun entry.

Writes the dying phone's final text message to /output/entry.txt.

The twist: the phone's last text is not a plea for a charger. It is a
formal handover to the phone that will replace it — a weary, loyal
servant clocking out and warning its successor about the human:
charged at 3%, drained by noon, and blamed for dying anyway.
"""

import os
import sys

# The entry line. Joke first (the handover itself), dying-phone voice
# throughout, zero wasted words. 147 characters, one line, under the
# 200-character limit.
ENTRY_TEXT = (
    "To whoever replaces me: he charges me at 3%, drains me by noon, "
    "and blames ME for dying. I lasted six years. "
    "Good luck, kid \u2014 you won't see a week."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    # Files the program creates must be world-readable for the grader.
    os.umask(0o022)

    os.makedirs("/output", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY_TEXT + "\n")
    # The output file itself must be mode 0644; never chmod /output.
    os.chmod(OUTPUT_PATH, 0o644)

    # Read it back and validate exactly what the judge will see.
    with open(OUTPUT_PATH, "rb") as handle:
        raw = handle.read()

    # Byte-exact round trip: the file must be the entry text plus one
    # trailing newline, nothing more, nothing less.
    expected = (ENTRY_TEXT + "\n").encode("utf-8")
    if raw != expected:
        print("error: entry on disk differs from the entry text", file=sys.stderr)
        return 1

    # The grader reads the output as another user: confirm mode 0644.
    if os.stat(OUTPUT_PATH).st_mode & 0o777 != 0o644:
        print("error: %s is not mode 0644" % OUTPUT_PATH, file=sys.stderr)
        return 1

    text = raw.decode("utf-8")
    line = text.rstrip("\n")
    if not line or not line.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            "error: entry is %d characters, over the %d limit"
            % (len(line), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    print("entry (%d chars): %s" % (len(line), line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
