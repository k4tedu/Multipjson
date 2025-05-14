import json
import argparse
from multipjson.update_check import check_for_updates


def print_banner():
    try:
        with open("ascii_logo.txt", "r") as logo:
            print(logo.read())
    except FileNotFoundError:
        print("multipjson - Multiple JSON Generator")

def generate_json_objects():
    check_for_updates("1.0.0")  # auto-update check
    print_banner()

    parser = argparse.ArgumentParser(
        description="Generate a list of JSON objects with auto-incremented or custom values."
    )
    parser.add_argument('-n', '--number', type=int, required=True, help="Number of JSON objects to generate")
    parser.add_argument('-f', '--fields', type=str, required=True, help="Comma-separated field names (e.g., name,email)")
    parser.add_argument('-v', '--values', type=str, required=True, help="Comma-separated base values (e.g., user,test)")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file name (e.g., output.json)")
    parser.add_argument('--prefix', type=str, default="", help="Prefix added before each value (optional)")
    parser.add_argument('--suffix', type=str, default="", help="Suffix added after each value (optional, default: index number)")

    args = parser.parse_args()

    field_names = [f.strip() for f in args.fields.split(',')]
    base_values = [v.strip() for v in args.values.split(',')]

    if len(field_names) != len(base_values):
        print("❌ The number of fields must match the number of base values.")
        return

    json_array = []
    for i in range(1, args.number + 1):
        item = {}
        for field, base in zip(field_names, base_values):
            suffix = args.suffix if args.suffix else str(i)
            item[field] = f"{args.prefix}{base}{suffix}"
        json_array.append(item)

    try:
        with open(args.output, 'w') as f:
            json.dump(json_array, f, indent=2)
        print(f"\n✅ Successfully generated {args.number} JSON objects to '{args.output}'.")
    except Exception as e:
        print(f"❌ Failed to write to file: {e}")

if __name__ == "__main__":
    generate_json_objects()


def main():
    generate_json_objects()
