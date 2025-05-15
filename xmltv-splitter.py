#!/usr/bin/env python3
"""
xmltv-splitter.py - Filter XMLTV EPG files by channel names, with optional remote URL download.

Copyright (c) 2025 suuhm
"""

from lxml import etree
import argparse
import re
import tempfile
import os
import urllib.request

def parse_args():
    parser = argparse.ArgumentParser(description="Filter XMLTV EPG file for selected channels.")
    parser.add_argument('--input', help='Path to input XMLTV file')
    parser.add_argument('--output', required=True, help='Path to output filtered XMLTV file')
    parser.add_argument('--channels', required=True, help='Comma-separated list of channel names (e.g., RTL,ProSieben)')
    parser.add_argument('--url-extern', help='Optional: external URL to fetch XMLTV file from')
    return parser.parse_args()

def normalize_text(text):
    """Fix encoding issues where UTF-8 is misinterpreted as Latin-1."""
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text  # Return original if decoding fails

def download_file(url):
    """Download a file from a URL to a temporary file."""
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
    urllib.request.urlretrieve(url, tmp_file.name)
    print(f"📥 Downloaded: {url} → {tmp_file.name}")
    return tmp_file.name

def main():
    args = parse_args()

    # Determine input source
    input_file = args.input
    temp_download = None
    if args.url_extern:
        input_file = download_file(args.url_extern)
        temp_download = input_file

    # Parse channel filter list
    channel_names = {name.strip() for name in args.channels.split(',')}

    tree = etree.parse(input_file)
    root = tree.getroot()

    # Collect allowed channel IDs
    allowed_ids = set()
    for channel in root.findall("channel"):
        display_name_el = channel.find("display-name")
        if display_name_el is not None:
            name = normalize_text(display_name_el.text.strip())
            if name in channel_names:
                allowed_ids.add(channel.get("id"))

    # Build filtered XMLTV structure
    new_root = etree.Element("tv", attrib=root.attrib)

    for channel in root.findall("channel"):
        if channel.get("id") in allowed_ids:
            new_root.append(channel)

    for programme in root.findall("programme"):
        ch_id = programme.get("channel")
        stop_time = programme.get("stop", "")
        if ch_id in allowed_ids:
            if stop_time == "19700101000000 +0000":
                programme.attrib.pop("stop", None)
            for elem in programme.iter():
                if elem.text:
                    elem.text = normalize_text(elem.text)
            new_root.append(programme)

    # Write to output file
    with open(args.output, "wb") as f:
        f.write(etree.tostring(new_root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

    print(f"✅ Filtered XMLTV saved to: {args.output}")

    # Clean up downloaded file
    if temp_download:
        os.remove(temp_download)
        print(f"🧹 Removed temporary file: {temp_download}")

if __name__ == "__main__":
    main()
