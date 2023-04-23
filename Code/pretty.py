import json
import os
# Don't Actually use this. It makes your json files a lot bigger.
def pretty_print_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)

def main():
    dir_path = input("Enter the directory path containing JSON files: ")

    if not os.path.exists(dir_path):
        print(f"The specified directory does not exist: {dir_path}")
        return

    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):
            file_path = os.path.join(dir_path, filename)
            pretty_print_json(file_path)
            print(f"Pretty-printed: {file_path}")

if __name__ == "__main__":
    main()