# This script converts an SRT file to a text file with a single sentence per line.
import re

input_srt = "/set/path/to/srt/file.srt" # Replace with your SRT file path
output_srt = "/set/path/to/txt/file.txt" # Replace with your output file path


def process_srt(srt_file, output_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
    output_lines = []
    buffer = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Remove fragment numbers
        if line.isdigit():
            continue

        # Remove timestamps and mark scene breaks
        if pattern.search(line):
            # if buffer:
            #     output_lines.append(" ".join(buffer) + "\n")
            #     # output_lines.append("[...]\n\n")
            #     buffer = []
            continue

        # Merge lines, but add a newline after sentences ending with a period
        if buffer and not buffer[-1].endswith(('.', '!', '?', '”')):
            buffer[-1] += " " + line  # Continue sentence
        else:
            if buffer:
                output_lines.append(" ".join(buffer) + "\n")  # Ensure a line break after full sentences
            buffer = [line]

    # Add any remaining text to output
    if buffer:
        output_lines.append(" ".join(buffer) + "\n\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

process_srt(input_srt, output_srt)
print("Processing complete. Output saved to", output_srt)
