import subprocess
import time
import os
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

def run_command(command, capture_output=False):
    """Utility to run a shell command."""
    result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
    if capture_output:
        return result.stdout.strip()

def check_vastai_installed():
    """Check if Vast.ai CLI is installed and running."""
    try:
        result = subprocess.run("vastai help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if result.returncode != 0:
            print(Fore.RED + "Vast.ai CLI is not installed or not functioning. Please install and configure Vast.ai CLI.")
            exit(1)
    except FileNotFoundError:
        print(Fore.RED + "Vast.ai CLI is not installed or not functioning. Please install and configure Vast.ai CLI.")
        exit(1)
def generate_rsa_key():
    """Generate a Vast.ai compatible SSH RSA key pair and add the public key to Vast.ai, returning the SSH key ID."""
    keypair_path = os.path.join(os.getcwd(), "hashcrack")
    if not os.path.exists(keypair_path + ".pub"):
        subprocess.run(f"ssh-keygen -t rsa -f {keypair_path} -q -N ''", shell=True, check=True)
        subprocess.run(f"chmod 600 {keypair_path}*".format(keypair_path), shell=True, check=True)
        with open(keypair_path + ".pub", 'r') as pub_key_file:
            pub_key = pub_key_file.read().strip()
        print(Fore.GREEN + "Adding SSH key to Vast.ai...")
        result = subprocess.run(f"vastai create ssh-key \"{pub_key}\"", shell=True, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        print(output)
        return vast_ssh_key_id(output)

def vast_ssh_key_id(output):
    """Return the SSH key ID from the Vast.ai created ssh-key output."""
    if "'success': True" in output:
        id_start = output.find("'id': ") + len("'id': ")
        id_end = output.find(',', id_start)
        return output[id_start:id_end]
    return output[id_start:id_end]
def print_ascii_banner():
    banner = """
██╗  ██╗ █████╗ ███████╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗      █████╗ ██╗
██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝     ██╔══██╗██║
███████║███████║███████╗███████║██║     ██████╔╝███████║██║     █████╔╝█████╗███████║██║
██╔══██║██╔══██║╚════██║██╔══██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗╚════╝██╔══██║██║
██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗     ██║  ██║██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

# Call the function to print the banner
print_ascii_banner()
def main():
    check_vastai_installed()
    ssh_key_id = generate_rsa_key()


    parser = argparse.ArgumentParser(description=Fore.CYAN + "Crack hashes using Hashcat with a Vast.ai instance.")
    parser.add_argument("-hash-file", help=Fore.YELLOW + "Path to the hash file to be cracked.", required=True)
    parser.add_argument("-mode", help=Fore.YELLOW + "Hashcat mode to use.", required=True)
    parser.add_argument("-wordlist-url", help=Fore.YELLOW + "URL of the wordlist (e.g., https://example.com/wordlist.gz). Must be a tar.gz, zip, or 7z file.", required=False)
    parser.add_argument("-pre-wordlist-url", choices=["rockyou" , "seclists"], help=Fore.YELLOW + "Pre-defined wordlist options. Currently only rockyou and seclists is supported.", required=False)
    parser.add_argument("-seclist-path", help=Fore.YELLOW + "Path to the specific SecList file to use. Ex: Seclists/Passwords/seasons.txt", required=False)
    parser.add_argument("-ruleset", choices=["best64", "best66", "dive", "oneruletorulethemall"],help=Fore.YELLOW + "The ruleset to use when cracking the hash with hashcat.", required=False)
    
    
    args = parser.parse_args()

    hash_file = args.hash_file
    mode = args.mode
    wordlist_url = args.wordlist_url
    pre_wordlist_url = args.pre_wordlist_url
    ruleset = args.ruleset

    # Validate that at least one wordlist option is provided
    if wordlist_url is None and pre_wordlist_url is None:
        print(Fore.RED + "Error: You must provide either -wordlist-url or -pre-wordlist-url")
        parser.print_help()
        exit(1)

# List of pre-defined wordlists to use. 
    if pre_wordlist_url == "rockyou":
        wordlist_url = "https://gitlab.com/kalilinux/packages/wordlists/-/raw/kali/master/rockyou.txt.gz?inline=false"
    elif pre_wordlist_url == "seclists":
        wordlist_url = "https://github.com/danielmiessler/SecLists"

# List of rulesets to use.
    if ruleset == "best64": 
        ruleset = "hashcat/rules/best64"
    elif ruleset == "best66":
        ruleset = "hashcat/rules/best66"
    elif ruleset == "dive":
        ruleset = "hashcat/rules/dive" 
    elif ruleset == "oneruletorulethemall":
        #ruleset_url = "https://github.com/NotSoSecure/password_cracking_rules/raw/master/OneRuleToRuleThemAll.rule"
        ruleset_url = "https://github.com/NotSoSecure/password_cracking_rules.git"
        ruleset_filename = "OneRuleToRuleThemAll.rule"
        download_command = f"git clone {ruleset_filename} {ruleset_url}"
        run_command(download_command)
        ruleset = ruleset_filename

    # You can change the instance type to a differnt device if you want to use a more powerful instance and how many GPUs you want to use by changing the number in the num_gpus"
    print(Fore.GREEN + "Searching for an appropriate instance...")
    search_command = (
        "vastai search offers 'datacenter = True disk_space > 50 inet_down>1000 gpu_name = RTX_4090 num_gpus > 6' "
        "| awk 'NR > 1 {print $0 | \"sort -k10,10n\"}' | head -n 1 | awk '{ print $1 }'"
    )
    instance_id = run_command(search_command, capture_output=True)

    print(Fore.GREEN + "Creating the instance...")
    create_command = f"vastai create instance {instance_id} --disk 50 --image 'dizcza/docker-hashcat:cuda' --ssh"
    run_command(create_command)

    print(Fore.GREEN + "Waiting for the instance to be ready...")
    time.sleep(100)  # Wait for the instance to be ready

    print(Fore.GREEN + "Showing instances...")
    instances = run_command("vastai show instances", capture_output=True)
    print(Fore.BLUE + instances)

    print(Fore.GREEN + "Attaching the ssh key...")
    attach_command = (
        "vastai attach ssh $(vastai show instances | tail -n 1 | awk '{ print $1 }') {ssh_key_id}"
    )
    run_command(attach_command)

    print(Fore.GREEN + "Downloading wordlist...")
    instance_ssh_url_command = "vastai ssh-url $(vastai show instances | tail -n 1 | awk '{ print $1 }')"
    instance_ssh_url = run_command(instance_ssh_url_command, capture_output=True)
    print(instance_ssh_url)
    
    # Handle different wordlist types
    if pre_wordlist_url == "rockyou":
        rockyou_filename = "rockyou.txt.gz"
        rockyou_download_command = (
            f"ssh -i hashcrack -o StrictHostKeyChecking=no {instance_ssh_url} 'sudo apt -y install gzip 7zip nano git; wget -O {rockyou_filename} {wordlist_url}; mv rockyou.txt.gz\\?inline\\=false rockyou.txt.gz; gunzip rockyou.txt.gz'"
        )
        run_command(rockyou_download_command)
        wordlist_filename = "rockyou.txt"
    elif pre_wordlist_url == "seclists":
        seclists_download_command = (
            f"ssh -i hashcrack -o StrictHostKeyChecking=no {instance_ssh_url} 'sudo apt -y install gzip 7zip nano git; git clone {wordlist_url}'"
        )        
        run_command(seclists_download_command)
        wordlist_filename = args.seclist_path
    else:
        # Handle custom wordlist URL
        wordlist_filename = wordlist_url.split("/")[-1]
        if wordlist_url.endswith(".zip"):
            wordlist_download_command = (
                f"ssh -i hashcrack -o StrictHostKeyChecking=no {instance_ssh_url} 'sudo apt -y install gzip 7zip nano git; wget -O {wordlist_filename} {wordlist_url}; unzip {wordlist_filename}'"
            )
            run_command(wordlist_download_command)
        elif wordlist_url.endswith(".7z"):
            wordlist_download_command = (
                f"ssh -i hashcrack -o StrictHostKeyChecking=no {instance_ssh_url} 'sudo apt -y install gzip 7zip nano git; wget -O {wordlist_filename} {wordlist_url}; 7z x {wordlist_filename}'"
            )
            run_command(wordlist_download_command)
        else:
            wordlist_download_command = (
                f"ssh -i hashcrack -o StrictHostKeyChecking=no {instance_ssh_url} 'sudo apt -y install gzip 7zip nano git; wget -O {wordlist_filename} {wordlist_url}'"
            )
            run_command(wordlist_download_command)

    print(Fore.GREEN + "Starting a tmux session...")
    # Create a new tmux session or attach to existing one
    tmux_setup_commands = [
        'tmux new-session -d -s ssh_tmux 2>/dev/null || true',
        'tmux has-session -t ssh_tmux 2>/dev/null || tmux new-session -d -s ssh_tmux',
        'tmux set-option -t ssh_tmux remain-on-exit on'
    ]
    
    for cmd in tmux_setup_commands:
        login_command = f"ssh -i hashcrack {instance_ssh_url} '{cmd}'"
        run_command(login_command)
        time.sleep(1)  # Give tmux time to initialize

    instance_ssh_url_parts = instance_ssh_url.split('@')
    ssh_hostname = instance_ssh_url_parts[1].split(':')[0]
    ssh_port = instance_ssh_url_parts[1].split(':')[1]

    print(Fore.GREEN + "Uploading hash file...")
    vault_transfer_command = f"scp -P {ssh_port} -i hashcrack {hash_file} root@{ssh_hostname}:{hash_file}"
    run_command(vault_transfer_command)

    print(Fore.GREEN + "Running Hashcat...")
    if pre_wordlist_url == "seclists":
        seclist_path = args.seclist_path
        if ruleset:
            hashcat_command = (
                f"ssh -i hashcrack {instance_ssh_url} "
                f"'tmux send-keys -t ssh_tmux \"hashcat -a 0 -m {mode} {hash_file} {seclist_path} -r {ruleset} -o cracked.txt\" C-m'"
            )
        else:
            hashcat_command = (
                f"ssh -i hashcrack {instance_ssh_url} "
                f"'tmux send-keys -t ssh_tmux \"hashcat -a 0 -m {mode} {hash_file} {seclist_path} -o cracked.txt\" C-m'"
            )
    elif ruleset and wordlist_filename:
        hashcat_command = (
            f"ssh -i hashcrack {instance_ssh_url} "
            f"'tmux send-keys -t ssh_tmux \"hashcat -a 0 -m {mode} {hash_file} {wordlist_filename} -r {ruleset} -o cracked.txt\" C-m'"
        )
    elif ruleset:
        hashcat_command = (
            f"ssh -i hashcrack {instance_ssh_url} "
            f"'tmux send-keys -t ssh_tmux \"hashcat -a 0 -m {mode} {hash_file} -r {ruleset} -o cracked.txt\" C-m'"
        )
    else:
        hashcat_command = (
            f"ssh -i hashcrack {instance_ssh_url} "
            f"'tmux send-keys -t ssh_tmux \"hashcat -a 0 -m {mode} {hash_file} {wordlist_filename} -o cracked.txt\" C-m'"
        )
    
    print(Fore.CYAN + "Debug: Executing command: " + hashcat_command)
    run_command(hashcat_command)

    print(Fore.GREEN + "Checking if hashes have been cracked...")
    check_cracked_command = f"ssh -i hashcrack {instance_ssh_url} 'test -f cracked.txt && echo exists'"
    cracked_exists = run_command(check_cracked_command, capture_output=True).strip()

    print(Fore.GREEN + "Checking if Hashcat is running...")
    check_hashcat_command = f"ssh -i hashcrack {instance_ssh_url} 'ps aux | grep hashcat'"
    hashcat_running = run_command(check_hashcat_command, capture_output=True).strip()
    if hashcat_running == "":
        print(Fore.RED + "Hashcat is not running. Please check the instance and make sure the hashes have been loaded correctly.")
        exit(1)

    print(Fore.GREEN + "Checking if hashes have been cracked...")
    check_cracked_command = f"ssh -i hashcrack {instance_ssh_url} 'test -f cracked.txt && echo exists'"
    cracked_exists = run_command(check_cracked_command, capture_output=True).strip()

    if cracked_exists == "exists":
        print(Fore.GREEN + "Retrieving results...")
        retrieve_command = f"ssh -i hashcrack {instance_ssh_url} 'cat cracked.txt'"
        cracked_data = run_command(retrieve_command, capture_output=True)
        with open("cracked.txt", "w") as f:
            f.write(cracked_data)
        print(Fore.BLUE + cracked_data)
    else:
        print(Fore.RED + "No cracked hashes found.")

    input(Fore.YELLOW + "Press Enter to delete the instance...")

    print(Fore.GREEN + "Deleting the instance...")
    destroy_command = (
        "vastai destroy instance $(vastai show instances | tail -n 1 | awk '{ print $1 }')"
    )
    
    result = run_command(destroy_command, capture_output=True)
    if "destroying" in result:
        print(Fore.YELLOW + "Instance is being destroyed...")
        print(Fore.GREEN + "Deleting local ssh key files...")
        subprocess.run(f"rm -f ssh_*.json", shell=True, check=True)
        subprocess.run(f"rm -f hashcrack*", shell=True, check=True)
        print(Fore.RED + "Do not forget to remove your SSH key from your Vast.ai account!")
        print(Fore.GREEN + "Instance destroyed successfully.")
    else:
        print(Fore.RED + "Failed to destroy the instance. Please remove the instance in the web console or in through Vast.ai CLI.")
        print(Fore.RED + "Do not forget to remove your SSH key from your Vast.ai account!")
        exit(1)

if __name__ == "__main__":
    main()
