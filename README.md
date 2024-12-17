
# bowing to the AI Overlords....and Pry0cc/TJNull for getting this off the ground, and opening my eyes to the darkside of technology.
# HashCrack-AI 

## Purpose:
Hashcrack-AI is an automated python script that is designed to use GPU instances provided by https://vast.ai, to deploy a Dockerized Hashcat CUDA instance https://github.com/dizcza/docker-hashcat. Once the instance is deployed the script will upload the hash file, download the specified wordlist or it will download a wordlist onto the instance and will attempt to crack the hash.

This tool eliminates the complexity of manually configuring and launching GPU-powered environments for password cracking, enabling ethical hackers and penetration testers to focus on their engagements.

# Why Use Hashcrack-AI?

- Cost-Effective GPU Access: Vast.ai offers powerful GPU instances at competitive rates. Hashcrack-AI simplifies access to these resources, ensuring you can crack hashes without investing in expensive hardware.
- Time-Saving Automation: With this python script, you can deploy a pre-configured Hashcat instance tailored for high-performance password cracking, saving time on setup and configurations.
- Scalable Performance: Choose from a range of GPU options based on your project needs, scaling your computing power as necessary for large or complex hash cracking tasks.

# How does it work?

At the time of development, this script will work on Linux systems. This script has not been tested on any Windows Operating Systems.

1. Generates an SSH key (hashcrack, hashcrack.pub) and loads the SSH Key into your Vast AI account.
2. Uses Vast.ai to find an avaliable instance with the pre-selected GPU and the number of GPU devices.
3. Builds the instance using the Hashcat Cuda Docker Container https://github.com/dizcza/docker-hashcat
4. Installs the necessary packages needed to download the wordlists
5. Download's the custom wordlist or pre-set wordlist
6. Upload the file that contains the hash you want to attempt to crack
7. Create's a tmux session to run Hashcat to crack the hash.
8. If a cracked.txt file appears, the script will print the output of the hash with the cracked password.
9. If cracked.txt does not appear then the hash could not be cracked or an error could have occured.
10. Before destroying the instance, you can ssh into using the generated ssh key.
11. When you are done with the instance you can press "ENTER" and the script will terminate the instance when you are done with it.

# Package Requirements

```
pipx install vastai
```

# Setup Requirements: 

1. Create an account on https://vast.ai.
2. In the Billing section select "Add Credit" to add the amount of credit you want to utilize.
3. Under "Account" copy your API Key. The format of your key should look something like this: "2f51bcc1cb5ac169c9a4785b21d10d0ef4f4508a8924b5030b22253ca8ec0384"
4. Using the vastcli add your api-key into the program

```
$ vastai --api-key "2f51bcc1cb5ac169c9a4785b21d10d0ef4f4508a8924b5030b22253ca8ec0384"
```

5. You are ready to start cracking with Vast.ai!

# Installation:

```
$ git clone https://github.com/k3nundrum/hashcrack-ai.git
$ python hashcrack-ai.py -h

██╗  ██╗ █████╗ ███████╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗      █████╗ ██╗                                                                                                                        
██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝     ██╔══██╗██║                                                                                                                        
███████║███████║███████╗███████║██║     ██████╔╝███████║██║     █████╔╝█████╗███████║██║                                                                                                                        
██╔══██║██╔══██║╚════██║██╔══██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗╚════╝██╔══██║██║                                                                                                                        
██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗     ██║  ██║██║                                                                                                                        
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝                                                                                                                        
                                                                                                                                                                                                                
usage: hashcrack-ai.py [-h] -hash-file HASH_FILE -mode MODE [-wordlist-url WORDLIST_URL] [-pre-wordlist-url {rockyou,seclists}] -seclist-path SECLIST_PATH
                       [-ruleset {best64,best66,dive,oneruletorulethemall}]

Crack hashes using Hashcat with a Vast.ai instance.
                                                                                                                                                                                                                
options:                                                                                                                                                                                                        
  -h, --help            show this help message and exit                                                                                                                                                         
  -hash-file HASH_FILE  Path to the hash file to be cracked.                                                                                                                                                    
  -mode MODE            Hashcat mode to use.                                                                                                                                                                    
  -wordlist-url WORDLIST_URL                                                                                                                                                                                    
                        URL of the wordlist (e.g., https://example.com/wordlist.gz). Must be a tar.gz, zip, or 7z file.                                                                                         
  -pre-wordlist-url {rockyou,seclists}                                                                                                                                                                          
                        Pre-defined wordlist options. Currently only rockyou and seclists is supported.                                                                                                         
  -seclist-path SECLIST_PATH                                                                                                                                                                                    
                        Path to the specific SecList file to use. Ex: Seclists/Passwords/seasons.txt                                                                                                            
  -ruleset {best64,best66,dive,oneruletorulethemall}                                                                                                                                                            
                        The ruleset to use when cracking the hash with hashcat.                                                                                                                                 

```

# Need more firepower?

As of now, the script is set to search for instances that have six GPU's running RTX 4090's. This can be modified in the script depending on the GPU you want and the number of GPU's you want in your instance: 

```
    print(Fore.GREEN + "Searching for an appropriate instance...")
    search_command = (
        "vastai search offers 'datacenter = True disk_space > 50 inet_down>1000 gpu_name = RTX_4090 num_gpus > 6' "
        "| awk 'NR > 1 {print $0 | \"sort -k10,10n\"}' | head -n 1 | awk '{ print $1 }'"
    )
    instance_id = run_command(search_command, capture_output=True)
```

# Cracking Examples: 

- Cracking an NTLM V2 hash with a weakpass wordlist https://weakpass.com/download/2012/weakpass_4.txt.7z
```
$ python hashcrack-ai.py -hash-file hashes -mode 5600 -wordlist-url https://weakpass.com/download/2012/weakpass_4.txt.7z
```

- Cracking an NTLMv2 hash using the rockyou wordlist with the best64 ruleset

```
$ python hashcrack-ai.py -hash-file hashes -mode 5600 -pre-wordlist-url rockyou -ruleset base64
```

- Cracking an NTLMv2 hash using seclist
```
python hashcrack-ai.py -hash-file hashes -mode 5600 -pre-wordlist-url seclist -seclist-path Seclists/Passwords/seasons.txt
```

# Disclaimer:

By using Hashcrack-AI, you acknowledge and agree to the following terms:

Educational Use Only: Hashcrack-AI is intended solely for educational purposes and authorized security testing. It is not intended for illegal or unauthorized activities. Users must have explicit permission from the system owners before attempting to crack any password hashes or access any accounts.

No Unauthorized Use: The user is fully responsible for ensuring that their use of this script complies with all applicable laws, regulations, and ethical standards. The script should never be used for cracking passwords, accounts, or systems without explicit written consent from the owner.

No Liability for Expenses: The user acknowledges that any costs or expenses incurred through the use of Vast.ai or any other third-party services while using this script are their own responsibility. The script author is not responsible for any fees or charges that may arise from utilizing GPU instances or any other resources.

No Liability for Damage or Misuse: The user assumes all risks associated with the use of this script. The author or contributors of Hashcrack-AI will not be held liable for any damages, legal actions, or consequences that may result from misuse or unauthorized activities involving the script.

By proceeding with the use of this script, you confirm your understanding and acceptance of these terms. Always use this tool responsibly and within the boundaries of legal and ethical guidelines.

# License: 

This project is under the GPLv3 Licence: Refer to license for more information.

# Resources: 

- Vast AI Documentation: https://vast.ai/docs/overview/introduction
- Password cracking in the Cloud with Vast.ai: https://adamsvoboda.net/password-cracking-in-the-cloud-with-hashcat-vastai/

# Credit
- TJNull for the bulk of the python port.
- Pry for the bash version PoC
