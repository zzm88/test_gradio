import os
import compileall
import shutil
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(filename='compile_and_replace.log', level=logging.INFO, format='%(asctime)s - %(message)s')

test_dirc = r"C:\Users\Administrator\Documents\stable-diffusion-webui_may10\my_pyc\testfiles"

def count_py_files(directory):
    count = 0
    for _, _, files in os.walk(directory):
        count += sum(1 for file in files if file.endswith(".py"))
    return count

def compile_and_replace_py_files(directory, progress_bar):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                logging.info(f"Compiling {file_path}")
                compileall.compile_file(file_path)

                # Find the .pyc file in the __pycache__ directory
                file_base_name = os.path.splitext(file)[0]
                pycache_dir = os.path.join(root, "__pycache__")
                for pyc_file in os.listdir(pycache_dir):
                    if pyc_file.startswith(file_base_name):
                        pyc_path = os.path.join(pycache_dir, pyc_file)

                        # Move the .pyc file to the original location and rename it
                        new_pyc_path = os.path.join(root, file_base_name + ".pyc")
                        shutil.move(pyc_path, new_pyc_path)

                        # Remove the original .py file
                        os.remove(file_path)
                        break

                progress_bar.update(1)

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    if directory == "": # If the user presses enter without typing anything
        directory = test_dirc

    if os.path.exists(directory):
        print(f"Starting compilation in {directory}")
        logging.info(f"Starting compilation in {directory}")

        py_file_count = count_py_files(directory)
        with tqdm(total=py_file_count, desc="Compiling", unit="file") as progress_bar:
            compile_and_replace_py_files(directory, progress_bar)

        print("Python files have been compiled and replaced.")
        logging.info("Python files have been compiled and replaced.")
    else:
        print(f"The provided directory path '{directory}' does not exist. Please check the path and try again.")
        logging.error(f"The provided directory path '{directory}' does not exist.")
