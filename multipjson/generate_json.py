import json
import os
import argparse
import uuid
import random
from datetime import datetime
from colorama import init, Fore, Style
from multipjson.update_check import check_for_updates
from collections import OrderedDict


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

def build_json_array(total, fields, values, prefix="", suffix="", id_type="normal", email_domain="demo.org", phone_digits=12):
    field_names = [f.strip() for f in fields.split(',')]
    base_values = [v.strip() for v in values.split(',')]

    if len(field_names) != len(base_values):
        raise ValueError("The number of fields and values must match.")

    json_array = []
    for i in range(1, total + 1):
        item = OrderedDict()
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
    if not all([args.total, args.fields, args.values, args.output]):
        print(Fore.BLUE + "🔧 No arguments detected, entering interactive mode...\n" + Style.RESET_ALL)
        args.total = int(input("How many JSON objects? "))
        args.output = input("Output filename (e.g., output.txt): ").strip()
        args.fields = input("Enter field names (comma-separated): ").strip()
        args.values = input("Enter base values (comma-separated): ").strip()
        args.email_domain = input("Custom email domain? (default: demo.org): ").strip() or "demo.org"
        id_choice = input("ID type? (uuid/normal): ").strip().lower()
        args.id_type = id_choice if id_choice in ['uuid', 'normal'] else "normal"
        phone_input = input("Phone number digits? (default: 12): ").strip()
        args.phone_digits = int(phone_input) if phone_input.isdigit() else 12

    # Build JSON array
    try:
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
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}" + Style.RESET_ALL)
        return

    # Save output file
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, args.output)

    with open(output_path, 'w') as f:
        json.dump(json_array, f, indent=2)

    print(Fore.GREEN + f"\n✅ Successfully generated {args.total} JSON objects into '{output_path}'." + Style.RESET_ALL)


def main():
    generate_json_objects()

if __name__ == "__main__":
    main()
