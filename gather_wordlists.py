#!/usr/bin/env python3

import os
import subprocess
import requests

def get_filename_from_url(url):
    """Extract the filename from the download URL"""
    return url.split('/')[-1]

def wordlist_exists(filename):
    """Check if the wordlist already exists in the wordlists directory"""
    filepath = os.path.join('wordlists', filename)
    return os.path.exists(filepath)

def download_wordlist(name, download_link):
    filename = get_filename_from_url(download_link)
    if wordlist_exists(filename):
        print(f"\nSkipping {name}: File already exists")
        return True
    
    print(f"\nDownloading: {name}")
    try:
        subprocess.run(['wget', '-P', 'wordlists', download_link], check=True)
        print(f"Successfully downloaded: {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {name}: {e}")
        return False

def display_menu(wordlists):
    print("\n=== Weakpass Wordlist Downloader ===")
    print("\nAvailable wordlists sorted by top ratings:\n")
    for idx, (name, url) in enumerate(wordlists.items(), 1):
        filename = get_filename_from_url(url)
        status = "[Downloaded]" if wordlist_exists(filename) else "[Not Downloaded]"
        print(f"{idx}. {name} {status}")
    print("\n0. Download all wordlists")
    print("q. Quit")
    print("\nTo download a specific wordlist, please enter its corresponding number.")
    print("\n==================================")
    print("\nNOW GO AND TIP THE AWESOME CREATOR OF THIS SITE, YA FREELOADER!: \n(https://www.buymeacoffee.com/zzzteph")
    
def get_user_choice(max_choice):
    while True:
        choice = input(f"\nEnter your choice (0-{max_choice} or q to quit): ").lower()
        if choice == 'q':
            return 'q'
        try:
            num = int(choice)
            if 0 <= num <= max_choice:
                return num
        except ValueError:
            pass
        print(f"Please enter a number between 0 and {max_choice} or 'q' to quit")

def main():
    # Create wordlists directory if it doesn't exist
    os.makedirs('wordlists', exist_ok=True)

    # The wordlists we want to download with their direct links
    target_wordlists = {
        "10_million_password_list_top_10000.txt": "https://weakpass.com/download/48/10_million_password_list_top_10000.txt.gz",
        "hashesorg2019": "https://weakpass.com/download/1851/hashesorg2019.gz",
        "rockyou-60.txt": "https://weakpass.com/download/86/rockyou-60.txt.gz",
        "cyclone.hashesorg.hashkiller.combined.txt": "https://weakpass.com/download/1927/cyclone.hashesorg.hashkiller.combined.txt.7z",
        "cyclone_hk.txt": "https://weakpass.com/download/1928/cyclone_hk.txt.7z",
        "dictionary_private.dic": "https://weakpass.com/download/1930/dictionary_private.dic.7z",
        "hashkiller-dict.txt": "https://weakpass.com/download/1932/hashkiller-dict.txt.7z",
        "ignis-10K.txt": "https://weakpass.com/download/1934/ignis-10K.txt.7z",
        "kaonashi14M.txt": "https://weakpass.com/download/1938/kaonashi14M.txt.7z",
        "rockyou2021.txt": "https://weakpass.com/download/1943/rockyou2021.7z",
        "hashkiller24.txt": "https://weakpass.com/download/1978/hashkiller24.txt.7z",
        "hashmob.net.large.found.txt": "https://weakpass.com/download/1981/hashmob.net.large.found.txt.7z",
        "hashmob.net.medium.found.txt": "https://weakpass.com/download/1983/hashmob.net.medium.found.txt.7z",
        "hashmob.net.small.found.txt": "https://weakpass.com/download/1987/hashmob.net.small.found.txt.7z",
        "hashmob.net.user.found.txt": "https://weakpass.com/download/1989/hashmob.net.user.found.txt.7z",
        "weakpass_4.txt": "https://weakpass.com/download/2012/weakpass_4.txt.7z",
        "triple-h.txt": "https://weakpass.com/download/2018/triple-h.txt.7z",
        "piotrcki-wordlist-top10m.txt": "https://weakpass.com/download/2020/piotrcki-wordlist-top10m.txt.7z",
        "weakpass_4a.txt": "https://weakpass.com/download/2015/weakpass_4a.txt.7z"
    }

    while True:
        display_menu(target_wordlists)
        choice = get_user_choice(len(target_wordlists))
        
        if choice == 'q':
            print("\nExiting...")
            break
        elif choice == 0:
            print("\nDownloading all missing wordlists...")
            for name, download_link in target_wordlists.items():
                download_wordlist(name, download_link)
        else:
            # Get the name and link for the chosen wordlist
            name = list(target_wordlists.keys())[choice - 1]
            download_link = target_wordlists[name]
            download_wordlist(name, download_link)
        
        # Ask if user wants to continue
        if input("\nDo you want to download more wordlists? (y/n): ").lower() != 'y':
            print("\nExiting...")
            break

    print("\nDownload process completed!")

if __name__ == "__main__":
    main()