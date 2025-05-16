import json
import os
import argparse
import uuid
import random
from datetime import datetime
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

def get_random_value(base, index, phone_digits=12, email_domain=None, id_type="normal", name_value=None):
    base = base.lower()
    genders = ['Male', 'Female']
    statuses = ['Active', 'Inactive', 'Pending']
    first_names = ['john', 'jane', 'mike', 'anna', 'lisa', 'david', 'chris', 'sara', 'kevin', 'nina', 'ungke', 'utu', 'agus']

    if base == "uuid":
        return str(uuid.uuid4())
    elif base == "id":
        return str(uuid.uuid4()) if id_type == "uuid" else str(index)
    elif base == "name":
        return random.choice(first_names)
    elif base == "email":
        if name_value:
            username = f"{name_value}{random.randint(100, 999)}"
        else:
            username = f"user{index}{random.randint(100,999)}"
        domain = email_domain if email_domain else "demo.org"
        return f"{username}@{domain}"
    elif base == "phone":
        return f"+62{''.join(random.choices('0123456789', k=phone_digits))}"
    elif base == "gender":
        return random.choice(genders)
    elif base == "age":
        return random.randint(18, 65)
    elif base == "status":
        return random.choice(statuses)
    elif base == "date":
        return datetime.now().strftime("%Y-%m-%d")
    else:
        return f"{base}{index}"

def generate_json_objects():
    parser = argparse.ArgumentParser(
        prog="multipjson",
        usage="multipjson [options] -t TOTAL -f FIELDS -v VALUES -o OUTPUT | or just run 'multipjson'",
        description="Generate multiple JSON objects easily.",
        epilog="""Examples:
  multipjson                             # Run in interactive mode
  multipjson -t 10 -f id,name,email,age,gender,status,date -v id,name,email,age,gender,status,date -o output.txt
  multipjson -t 5 -f id,name,email,age,gender,status,date -v id,name,email,age,gender,status,date --id-type uuid/normal --email-domain my.com -o result.txt --prefix "" --suffix _v1
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-t", "--total", type=int, help="Number of JSON objects", required=False)
    parser.add_argument("-f", "--fields", help="Comma-separated field names", required=False)
    parser.add_argument("-v", "--values", help="Comma-separated base values for each field", required=False)
    parser.add_argument("-o", "--output", help="Output filename (e.g., output.txt)", required=False)
    parser.add_argument("-idt", "--id-type", choices=["uuid", "normal"], help="ID generation type", default="normal")
    parser.add_argument("-ed", "--email-domain", help="Custom email domain", default="demo.org")
    parser.add_argument("-pd", "--phone-digits", type=int, help="Number of digits for phone number", default=12)
    parser.add_argument("-pfx", "--prefix", help="Optional prefix for each field value", default="")
    parser.add_argument("-sfx", "--suffix", help="Optional suffix for each field value", default="")

    args = parser.parse_args()

    print_banner()
    check_for_updates()

    # Interactive fallback
    if not all(getattr(args, key, None) for key in ["total", "output", "fields", "values"]):
        print(Fore.BLUE + "🔧 No arguments detected, entering interactive mode...\n" + Style.RESET_ALL)
        args.total = int(input("How many JSON objects? "))
        args.output = input("Output filename (e.g., output.txt): ").strip()
        fields_input = input("Enter field names separated by commas (e.g., name,description): ").strip()
        values_input = input("Enter base values separated by commas (e.g., name,email): ").strip()

        args.email_domain = input("Custom email domain? (default: demo.org): ").strip() or "demo.org"
        id_choice = input("ID type? (uuid/normal): ").strip().lower()
        args.id_type = id_choice if id_choice in ['uuid', 'normal'] else "normal"
        phone_input = input("Phone number digits? (default: 12): ").strip()
        args.phone_digits = int(phone_input) if phone_input.isdigit() else 12
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
        name_value = None
        for field, base in zip(field_names, base_values):
            if base == "name":
                name_value = get_random_value(base, i)
                item[field] = f"{args.prefix}{name_value}{args.suffix}"
            elif base == "email":
                item[field] = get_random_value(base, i, email_domain=args.email_domain, name_value=name_value)
            elif base == "id":
                item[field] = get_random_value(base, i, id_type=args.id_type)
            elif base == "phone":
                item[field] = get_random_value(base, i, phone_digits=args.phone_digits)
            else:
                item[field] = f"{args.prefix}{get_random_value(base, i)}{args.suffix}"
        json_array.append(item)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, args.output)

    with open(output_path, 'w') as f:
        json.dump(json_array, f, indent=2)

    print(Fore.GREEN + f"\n✅ Successfully generated {args.total} JSON objects into '{output_path}'." + Style.RESET_ALL)

def main():
    generate_json_objects()
