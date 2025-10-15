#!/usr/bin/python3

import sys
import json
import re

query = sys.argv[1]
markdown_file = "/Users/currant/Documents/Lebowski/TBL.md" # Replace with your file path

try:
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    items = []
    found_indices = []

    for i, line in enumerate(lines):
        if query.lower() in line.lower() and line.strip():
            found_indices.append(i)

    if found_indices:
        for index in found_indices:
            matching_line = lines[index].strip()
            line_number = index + 1
            context_lines = lines[max(0, index - 3):min(len(lines), index + 4)]
            context_text = '\n'.join(context_lines)
            
            # --- Find the full sentence ---
            full_sentence = matching_line # Default to the full line
            # Split the line into sentences and find the one with the query
            sentences = re.findall(r'[^.!?]+[.!?]?', matching_line)
            for sentence in sentences:
                if query.lower() in sentence.lower():
                    full_sentence = sentence.strip()
                    break
            # -----------------------------

            items.append({
                "title": matching_line,
                # Subtitle updated for new default action
                "subtitle": "Press ↩ to copy sentence. Press ⇧ to open in editor.",
                # Arg is now the full sentence for the default action
                "arg": full_sentence,
                "preview": context_text,
                "text": {
                    "copy": context_text,
                    "largetype": context_text
                },
                "mods": {
                    "shift": {
                        "valid": True,
                        # Shift-arg is now the file path and line number
                        "arg": f"{markdown_file}:{line_number}",
                        # Subtitle updated for new shift action
                        "subtitle": f"Open in editor at line {line_number}"
                    }
                }
            })
        
        print(json.dumps({"items": items}))
    else:
        print(json.dumps({"items": [{"title": "No results found."}]}))

except FileNotFoundError:
    print(json.dumps({"items": [{"title": "Markdown file not found.", "subtitle": markdown_file}]}))
except Exception as e:
    print(json.dumps({"items": [{"title": "An error occurred.", "subtitle": str(e)}]}))