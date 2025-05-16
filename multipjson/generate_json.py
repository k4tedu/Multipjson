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
        usage="multipjson [options] -t TOTAL -f FIELDS -v VALUES -o OUTPUT",
        description="Generate multiple JSON objects easily.",
        epilog="""Examples:
  multipjson                             # Run in interactive mode
  multipjson -t 10 -f id,name,email -v id,name,email -o output.json
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-t", "--total", type=int, help="Number of JSON objects", required=False)
    parser.add_argument("-f", "--fields", help="Comma-separated field names", required=False)
    parser.add_argument("-v", "--values", help="Comma-separated base values", required=False)
    parser.add_argument("-o", "--output", help="Output filename (e.g., output.json or output.txt)", required=False)
    parser.add_argument("-idt", "--id-type", choices=["uuid", "normal"], help="ID generation type", default="normal")
    parser.add_argument("-ed", "--email-domain", help="Custom email domain", default="demo.org")
    parser.add_argument("-pd", "--phone-digits", type=int, help="Phone number digit count", default=12)
    parser.add_argument("-pfx", "--prefix", help="Prefix to add", default="")
    parser.add_argument("-sfx", "--suffix", help="Suffix to add", default="")

    args = parser.parse_args()

    print_banner()
    check_for_updates()

    if not all([args.total, args.fields, args.values, args.output]):
        print(Fore.BLUE + "🔧 No arguments detected, entering interactive mode...\n" + Style.RESET_ALL)
        args.total = int(input("How many JSON objects? "))

        # Ask for output format
        output_format = input("Output format? (json/txt) [json]: ").strip().lower()
        if output_format not in ["json", "txt"]:
            output_format = "json"
        args.output = input(f"Output filename (e.g., output.{output_format}): ").strip()
        if not args.output.endswith(f".{output_format}"):
            args.output = f"{args.output}.{output_format}"

        args.fields = input("Enter field names (comma-separated): ").strip()
        args.values = input("Enter base values (comma-separated): ").strip()
        id_type_input = input("ID type? (uuid/normal) [normal]: ").strip().lower()
        args.id_type = id_type_input if id_type_input in ["uuid", "normal"] else "normal"
        domain_input = input("Custom email domain? (default: demo.org): ").strip()
        args.email_domain = domain_input if domain_input else "demo.org"
        phone_digits_input = input("Phone number digits? (default: 12): ").strip()
        args.phone_digits = int(phone_digits_input) if phone_digits_input.isdigit() else 12

    field_names = [f.strip() for f in args.fields.split(',')]
    base_values = [v.strip() for v in args.values.split(',')]

    if len(field_names) != len(base_values):
        print(Fore.RED + "❌ Field count doesn't match value count." + Style.RESET_ALL)
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

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", args.output)

    if args.output.endswith(".json"):
        with open(output_path, "w") as f:
            json.dump(json_array, f, indent=2)
    elif args.output.endswith(".txt"):
        with open(output_path, "w") as f:
            for entry in json_array:
                f.write(json.dumps(entry) + "\n")

    print(Fore.GREEN + f"\n✅ Successfully generated {args.total} JSON objects into '{output_path}'." + Style.RESET_ALL)

def main():
    generate_json_objects()

if __name__ == "__main__":
    main()
