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
    parser.add_argument("-f", "--fields", help="Comma-separated field names", required=False)
    parser.add_argument("-v", "--values", help="Comma-separated base values for each field", required=False)
    parser.add_argument("--prefix", help="Optional prefix for each field value", default="")
    parser.add_argument("--suffix", help="Optional suffix for each field value", default="")

    args = parser.parse_args()

    check_for_updates()

    # fallback ke input manual jika argumen tidak lengkap
    if not all(getattr(args, key, None) for key in ["total", "output", "fields", "values"]):
        args.total = int(input("How many JSON objects? "))
        args.output = input("Output filename (e.g., output.txt): ").strip()
        fields_input = input("Enter field names separated by commas (e.g., name,description): ").strip()
        values_input = input("Enter base values separated by commas (e.g., user,desc): ").strip()
    else:
        fields_input = args.fields
        values_input = args.values

    field_names = [f.strip() for f in fields_input.split(',')]
    base_values = [v.strip() for v in values_input.split(',')]

    if len(field_names) != len(base_values):
        print(Fore.RED + "❌ The number of fields and values must match." + Style.RESET_ALL)
        return

    json_array = []
    for i in range(1, args.total + 1):
        item = {}
        for field, base in zip(field_names, base_values):
            item[field] = f"{args.prefix}{base}{i}{args.suffix}"
        json_array.append(item)

    with open(args.output, 'w') as f:
        json.dump(json_array, f, indent=2)

    print(Fore.GREEN + f"\n✅ Successfully generated {args.total} JSON objects into '{args.output}'." + Style.RESET_ALL)

def main():
    print_banner()
    generate_json_objects()
