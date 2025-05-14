import json
import os
import argparse
from colorama import init, Fore, Style
from multipjson.update_check import check_for_updates

def print_banner():
    init(autoreset=True)
    print(Fore.CYAN + r"""
  __  __       _ _   _       _                  
 |  \/  |_   _| | |_(_)_ __ (_)___  ___  _ __   
 | |\/| | | | | | __| | '_ \| / __|/ _ \| '_ \  
 | |  | | |_| | | |_| | |_) | \__ \ (_) | | | | 
 |_|  |_|\__,_|_|\__|_| .__// |___/\___/|_| |_|  v1.0.0
                      |_| |__/                  
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "        Created by k4tedu\n" + Style.RESET_ALL)

def generate_json_objects():
    parser = argparse.ArgumentParser(description="Generate multiple JSON objects easily.")
    parser.add_argument("-t", "--total", type=int, help="Number of JSON objects", required=False)
    parser.add_argument("-o", "--output", help="Output filename (e.g., output.txt)", required=False)
    parser.add_argument("--fields", help="Comma-separated field names", required=False)
    parser.add_argument("--values", help="Comma-separated base values for each field", required=False)
    parser.add_argument("--prefix", help="Optional prefix for each field value", default="")
    parser.add_argument("--suffix", help="Optional suffix for each field value", default="")

    args = parser.parse_args()

    check_for_updates()

    if not (args.total and args.filename and args.fields and args.values):
        # interactive fallback
        args.total = int(input("How many JSON objects? "))
        args.filename = input("Output filename (e.g., output.txt): ").strip()
        fields_input = input("Enter field names separated by commas (e.g., name,description): ").strip()
        values_input = input("Enter base values separated by commas (e.g., user,desc): ").strip()
    else:
        fields_input = args.fields
        values_input = args.values

    field_names = [x.strip() for x in fields_input.split(',')]
    base_values = [x.strip() for x in values_input.split(',')]

    if len(field_names) != len(base_values):
        print("❌ Number of fields and values must match.")
        return

    json_array = []
    for i in range(1, args.total + 1):
        item = {}
        for field, base in zip(field_names, base_values):
            item[field] = f"{args.prefix}{base}{i}{args.suffix}"
        json_array.append(item)

    with open(args.filename, 'w') as f:
        json.dump(json_array, f, indent=2)

    print(f"\n✅ Successfully generated {args.total} JSON objects into '{args.filename}'.")

def main():
    print_banner()
    generate_json_objects()
