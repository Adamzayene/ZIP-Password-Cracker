#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import zipfile
import argparse
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from colorama import init, Fore, Style

intro = f"""
{Fore.CYAN}███████╗██╗██████╗          ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
{Fore.CYAN}╚══███╔╝██║██╔══██╗        ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
{Fore.CYAN}  ███╔╝ ██║██████╔╝        ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
{Fore.CYAN} ███╔╝  ██║██╔═══╝         ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
{Fore.BLUE}███████╗██║██║     ███████╗╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
{Fore.BLUE}╚══════╝╚═╝╚═╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                   
{Style.RESET_ALL}
{Fore.YELLOW}Developed by: {Fore.GREEN}Adam Zayene(Black_Shadow){Style.RESET_ALL}
"""

def setup_logger():
    """Setup logger for the application."""
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def extract_file(zfile, password, found_event, extract_path="."):
    """Attempt to extract the ZIP file using the provided password."""
    if found_event.is_set():
        return None
    try:
        zfile.extractall(path=extract_path, pwd=password.encode('utf-8'))
        logging.info(f'[+] Password found: {Fore.GREEN}{password}{Style.RESET_ALL}')
        found_event.set()
        return password
    except (RuntimeError, zipfile.BadZipFile):
        return None
    except FileExistsError:
        logging.warning("File or directory already exists. Extraction skipped.")
        return None

def crack_zip_password(zip_path, dict_path, max_workers=10):
    """Main function to crack ZIP password using dictionary attack."""
    logging.info(f"Starting attack on ZIP file: {zip_path}")
    found_event = Event()

    with zipfile.ZipFile(zip_path) as zfile:
        with open(dict_path, 'r', encoding='latin-1', errors='ignore') as passfile:
            passwords = (line.strip() for line in passfile)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for password in passwords:
                    if found_event.is_set():
                        break
                    future = executor.submit(extract_file, zfile, password, found_event, extract_path=zip_path.stem)
                    futures.append(future)
                
                for future in futures:
                    result = future.result()
                    if result:
                        return result
                
                if not found_event.is_set():
                    logging.warning("Password not found in dictionary.")
    return None

def main():
    """Parse arguments and initiate the password cracking process."""
    parser = argparse.ArgumentParser(
        description="Advanced ZIP file password cracker using a dictionary attack."
    )
    parser.add_argument('-f', '--file', required=True, type=Path,
                        help='Path to the zip file')
    parser.add_argument('-d', '--dictionary', required=True, type=Path,
                        help='Path to the dictionary file')
    parser.add_argument('-w', '--workers', type=int, default=10,
                        help='Number of threads to use (default is 10)')
    
    args = parser.parse_args()
    
    # Validate paths
    if not args.file.is_file():
        logging.error(f"The specified zip file does not exist: {args.file}")
        exit(1)
    if not args.dictionary.is_file():
        logging.error(f"The specified dictionary file does not exist: {args.dictionary}")
        exit(1)
    
    # Setup logger
    setup_logger()

    # Initialize colorama
    init(autoreset=True)
    
    # Print the intro
    print(intro)
    
    # Start the cracking process
    logging.info("Password cracking initiated...")
    result = crack_zip_password(args.file, args.dictionary, args.workers)
    
    if result:
        logging.info(f"Cracking complete. The password is: {Fore.GREEN}{result}{Style.RESET_ALL}")
    else:
        logging.warning("Cracking failed. No valid password found.")

if __name__ == '__main__':
    main()
