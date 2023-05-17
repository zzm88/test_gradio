import os
import python_obfuscator

def obfuscate_code(code):
    obfuscator = python_obfuscator.obfuscator()
    obfuscated_code = obfuscator.obfuscate(code)
    return obfuscated_code

def get_file_contents(filename):
    with open(filename, 'r') as file:
        contents = file.read()
    return contents

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.abspath(__file__))
    key_filename = os.path.join(current_directory, 'key.py')
    secret_key_filename = os.path.join(current_directory, 'secret_key.py')

    if os.path.exists(key_filename):
        key_code = get_file_contents(key_filename)
        obfuscated_code = obfuscate_code(key_code)
        save_to_file(secret_key_filename, obfuscated_code)
        print(f"Obfuscated code saved to {secret_key_filename}.")
    else:
        print(f"File {key_filename} not found.")