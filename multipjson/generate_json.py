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
    first_names = ['john', 'jane', 'mike', 'anna', 'lisa', 'david', 'chris', 'sara', 'kevin', 'nina', 'ungke', 'utu', 'agus', 'mince', 'bambang']

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

def build_json_array(total, fields, values, prefix='', suffix='', id_type='normal', email_domain='demo.org', phone_digits=12):
    field_names = [f.strip() for f in fields.split(',')]
    base_values = [v.strip() for v in values.split(',')]

    if len(field_names) != len(base_values):
        raise ValueError("The number of fields and values must match.")

    json_array = []
    for i in range(1, total + 1):
        item = {}
        name_value = None
        for field, base in zip(field_names, base_values):
            if base == "name":
                name_value = get_random_value(base, i)
                item[field] = f"{prefix}{name_value}{suffix}"
            elif base == "email":
                item[field] = get_random_value(base, i, email_domain=email_domain, name_value=name_value)
            elif base == "id":
                item[field] = get_random_value(base, i, id_type=id_type)
            elif base == "phone":
                item[field] = get_random_value(base, i, phone_digits=phone_digits)
            else:
                item[field] = f"{prefix}{get_random_value(base, i)}{suffix}"
        json_array.append(item)
    return json_array

def generate_json_objects():
    parser = argparse.ArgumentParser(
        description="Generate multiple JSON objects easily.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-t", "--total", type=int, help="Number of JSON objects")
    parser.add_argument("-f", "--fields", help="Comma-separated field names")
    parser.add_argument("-v", "--values", help="Comma-separated base values for each field")
    parser.add_argument("-o", "--output", help="Output filename (e.g., output.json)", default="output.json")
    parser.add_argument("-idt", "--id-type", choices=["uuid", "normal"], default="normal")
    parser.add_argument("-ed", "--email-domain", default="demo.org")
    parser.add_argument("-pd", "--phone-digits", type=int, default=12)
    parser.add_argument("-pfx", "--prefix", default="")
    parser.add_argument("-sfx", "--suffix", default="")

    args = parser.parse_args()

    print_banner()
    check_for_updates()

    if not all([args.total, args.fields, args.values]):
        print(Fore.BLUE + "🔧 No arguments detected, entering interactive mode...\n" + Style.RESET_ALL)
        args.total = int(input("How many JSON objects? "))
        args.fields = input("Enter field names (comma-separated): ").strip()
        args.values = input("Enter base values (comma-separated): ").strip()

    json_array = build_json_array(
        total=args.total,
        fields=args.fields,
        values=args.values,
        prefix=args.prefix,
        suffix=args.suffix,
        id_type=args.id_type,
        email_domain=args.email_domain,
        phone_digits=args.phone_digits
    )

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", args.output)
    with open(output_path, 'w') as f:
        json.dump(json_array, f, indent=2)

    print(Fore.GREEN + f"\n✅ Successfully generated {args.total} JSON objects into '{output_path}'." + Style.RESET_ALL)

def main():
    generate_json_objects()
