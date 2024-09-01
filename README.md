# ZIP-Password-Cracker
This tool is designed to crack the password of ZIP files using a dictionary attack. It reads passwords from a dictionary file and attempts to extract the ZIP file using each password until the correct one is found.

## Features
- **Multithreading:** Increases the speed of the attack by utilizing multiple threads.
- **Logging:** Logs execution information and displays results in an organized log.
- **Colored Output:** Highlights important results, such as the correct password, using different colors.
- **Customizable:** You can adjust the number of threads used according to your system’s capabilities.

## How to Download and Use

### 1. Download the Tool from GitHub

To download the tool, clone the repository from GitHub using the following command:

```bash
git clone https://github.com/Adamzayene/zip-password-cracker.git
```
### 2.Then navigate to the tool's directory:
```bash
cd zip-password-cracker
```
## How to Use
To use the tool for cracking a ZIP file password, run the following command:
```bash
python3 extract.py -f <path_to_zip_file> -d <path_to_dictionary_file> -w <number_of_threads>
```
- **<path_to_zip_file>:** The path to the ZIP file you want to crack.
- **<path_to_dictionary_file>:** The path to the dictionary file containing the list of passwords.
- **<number_of_threads>:** The number of threads you want to use.
## Contributing
If you want to contribute to the development of the tool, you can fork the repository, make the necessary changes, and then submit a pull request to have your changes merged.
