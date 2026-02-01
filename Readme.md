[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/WrWEa-TD)
# Homework 4: Parallel Kaminsky Attack

K-POP group New Jeans and their record label, HYBE, have been involved in a brutal and bitter public battle over the group's freedom to use their name and exit from their contract with the label.

In the latest escalation of this conflict, HYBE has deployed a centralized DNS system to ensure that all traffic to New Jeans-related websites is routed through their controlled servers. Any fan attempting to visit a New Jeans website is unknowingly directed to HYBE-approved content.

However, you, a devoted New Jeans fan, have discovered a weakness in HYBE’s DNS resolver - the Parallel Kaminsky Attack. By overwhelming the resolver with forged DNS responses, you can poison its cache and redirect unsuspecting fans to a true New Jeans-controlled website.

To complete your mission, you have been secretly provided with an executable containing HYBE's DNS Server and name server. This name server remains the same for every outgoing request, a crucial detail that will aid in your attack.

## Grading

In this assignment, you have been provided test cases for task 2 and 3. Do not assume that your code will be tested _exclusively_ against these test cases. We reserve the right to use any test cases which conform to the specification provided for these tasks as part of grading this assignment, and you should expect for there to be a few additional test cases for each task which you are not aware of.

## GitHub Classroom

For this assignment, we are using GitHub Classroom to manage your submissions.

### How to Join

Click [THIS LINK](https://classroom.github.com/a/WrWEa-TD) to join the GitHub Classroom.

If prompted, log in to your GitHub account. If you don’t have one, you’ll need to create a free account.
Associate your GitHub login with your NetID using the menu.

### Accepting the Assignment

After joining, you will see an option to accept the Homework 4 assignment.

This will automatically create a private repository for you under the classroom organization.

You will have full access to this repository to manage your code.

### Submitting Your Work

Submit Task 2 and Task 3 by committing and pushing your work to this repository.

Make sure your latest changes are pushed before the deadline.

You can verify your submission by checking your repository on GitHub.

If you need help with GitHub/git basics (cloning, committing, pushing), refer to [GitHub Docs](https://docs.github.com/en).

## Installation:

You will install a virtual machine to run Kali linux, and work/test your code with the resolver
executable provided to you. Your program will be evaluated on 64-bit Kali Linux 2024.4.

1. First, assess whether your computer utilizes ARM architecture (for example, M1 Mac devices) or
x86 (Intel, AMD, etc). This will determine what VM and executable you will use.

    #### Apple Silicon Installation Instructions
    1. Go to https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion and install a 
    Virtual Machine. If you are on an ARM device, you will install VMware Fusion Pro. This software is free.

    2. Register for a Broadcom account. You can skip `Build My Profile`

    3. Go to `My Downloads` and press `Free Software Downloads Available HERE`
        1. Go to VMware Fusion
        2. Select version 13.6.3
        3. Agree to the terms and conditions, and then press on the cloud download icon
        4. Once the DMG is installed onto your device, double click on it and follow the insutructions to add it to your device.
        5. You will be asked to enter license key. Select VMware Fusion Pro for Personal Use.
        6. You will need to allow VMware fusion to have disk access to your device. Go to security & privacy and add it yourself if necessary.

    #### x86 Installation Instructions
    1. Download VirtualBox or VMware or Qemu follow the setup instructions to use it in next steps for kali linux installation.

2. Go to https://old.kali.org/base-images/kali-2024.4/
    #### Apple Silicon Installation Instructions
    1. Download the recommended installer. It should be the installer arm64 ISO
    2. Once it finishes downloading, open VMware Fusion and drag and drop the ISO. 
    3. Select Debian 12.x 64 bit ARM
    4. Press finish and follow the graphical set up instructions for your new virtual machine

    #### x86 Installation Instructions
    1. Download the recommended installer. It should be the installer amd64 ISO
    2. Once it finishes downloading, open VMware Fusion/Virtual Box/Qemu and drag and drop the ISO. 
    3. Select Debian 12.x 64 bit
    4. Press finish and follow the graphical set up instructions for your new virtual machine

> [!NOTE]  
> You may find it convenient to SSH into the VM to work on the assignment through your local machine with something like VS Code. Here are some steps you may find useful for this
> 1. sudo apt install openssh-server
> 2. sudo systemctl start ssh
> 3. ifconfig # find your local ip this way. It will be under eth0
>
> Now you can ssh into the VM from your device (or VSCode or any other IDE)

3. Clone your repository onto the Virtual Machine. There are two executables, one built for ARM `dns-server-arm` and one built for x86 `dns-server-x86`. Use whichever is appropriate in your situation to run locally. 

## Explanation of Repo:

You have been provided with the following files in this repository

    - dns-server-arm
    - dns-server-x86
    - dns-server-arm-test
    - dns-server-x86-test
    - .github/workflows/classroom.yml
    - settings.json
    - task2/
        - tests/output.txt
        - tests/score.txt
        - build.sh
        - pada
        - tests.json
    - task3/
        - tests/output.txt
        - tests/score.txt
        - build.sh
        - kaminsky
        - tests.json

You will use `settings.json` to set various parameters in order to assist you with debugging. There are 4 parameters available for modification in this file

    # transaction ids for outgoing requests
    transaction_id:  
        -1: will set a random transaction id
        0: See 1B
        >0: Fixed transaction ID (ie setting to 1234 means that all outgoing transaction ids will be 1234)
    
    # This is the delay in milliseconds for the dns to send an outgoing request (for you to be able to debug attacking it)
    response_delay:
        -1: Never send outgoing request
        >-1: Delay in milliseconds
    
    port: set this to any port you would like the DNS server to run on 

    # this executable runs both a dns resolver, and a nameserver which it forwards requests to. 
    ns_port: set this to any port you would like the name server to run on

    pada: location of pada executable. Should always be "task2/pada"

    kaminsky: location of kaminsky executable. Should always be "task3/kaminsky"

You should run the dns-server executable in the same directory as the settings.json file in order to start the local dns resolver. 

The folders Task2 and Task3 are given for you to write your code responses to Task 2 and 3 of this assignment. You are given test files which you can use to test the functionality of your code against the provided DNS server (using the test executable). You are encouraged to write your own tests.

We have provided some test cases for you in the classroom.yml file which show the expected output for some basic functionality.

## [15 Points] Task 1: HYBE DNS Resolver Analysis 

HYBE has deployed a centralized DNS infrastructure to control all traffic related to New Jeans. However, before launching an attack, you need to analyze how their DNS resolver behaves.

You have been provided access to HYBE's local DNS resolver through GitHub classroom, which you can run locally. Using network analysis tools like tcpdump or Wireshark, you must gather intelligence on how this resolver handles DNS queries. Your findings will be crucial for later tasks, where you will attempt to poison its cache.

You will submit this task on Brightspace as a text file titled `<Student-ID>-<Last Name>-<First Name>.txt`. 

***Submitting anything other than a text file on brightspace will result in an automatic zero for this section*** 

You can make a query to the DNS resolver using 
`dig @localhost -p <port> hybecorp.com`

### Executable

Please write which executable you used for this assignment, `dns-server-arm` or `dns-server-x86`

### 1a. Name Server

I. What external DNS server does the nameserver send outbound requests to?

II. What is the name of the nameserver that the provided resolver forwards every DNS query to?

### 1b. Transaction IDs

Go to `settings.json` and set `transaction_id=0`.
Observe the pattern of the transaction id for each outbound request to the DNS server, and how it changes with each outbound request. Describe the observed behavior.

### 1c. Error Handling

I. List 2 query record types that this DNS server supports

II. List 2 query record types the DNS server does not support

III. What error do you get when you send a malformed packet? 

## [35 Points] Task 2: Pada Packet Transmitter

Your next step in dismantling HYBE's DNS control is to develop a powerful tool that allows you to create DNS packets.

In a normal DNS exchange, resolvers and name servers communicate using a well-defined structure containing transaction IDs, response codes, and additional metadata. However, to execute your attack successfully, you need to craft and modify these packets manually.

To achieve this, you will create a Command Line Interface (CLI) tool called "Pada", which allows you to generate and send customized DNS packets.

#### Included files

`task2/build.sh` - this file will compile your code so that we can run and test it 

`task2/pada` - this will be the name of the executable file generated by `task2/build.sh` for us to run & test

#### Restrictions

You are allowed to use whatever libraries you would like as part of the CLI (ie parsing flags and arguments). Scapy in Python and meikg/dns in Go are allowed.

#### Usage
```
pada [OPTIONS] <query_name> <dns_server>
```

#### Options

| Option | Description | Example |
|--------|-------------|---------|
| `-p, --port <port>` | Specify destination port (default: 53) | `pada -p 5353 hybecorp.com localhost` |
| `-q, --query` | Send as query packet (default) | `pada -q hybecorp.com localhost` |
| `-r, --response` | Send as response packet | `pada -r hybecorp.com localhost` |
| `-c, --rcode <code>` |Set response code (0-15) (default: 0) | `pada -r -c 3 hybecorp.com localhost` |
| `-t, --txid <id>` | Set transaction ID (0-65535) (default: any) | `pada -t 1234 hybecorp.com localhost` |
| `-i, --ipaddr <address>` | IP address to include in response  | `pada -r -i 192.168.1.10 hybecorp.com localhost` |
| `-n, --ns <nameserver>` | Nameserver to include in response | `pada -r -n ns1.hybecorp.com localhost` |

> [!NOTE]  
> 1. You must have appropriate permissions on your device to send packets on the specified ports
> 2. You can assume that only -r or -q will be run at one time, not both at the same time
> 3. You are only required to support A records for this tool (for requests and responses)
> 4. You are only __*sending*__ packets, do not wait for a server response
> 5. `-i` and `-n` expect you to create an answer/authority record

- `<query_name>`: The domain name to query (e.g., hybecorp.com)
- `<dns_server>`: IP address of the DNS server to send the packet to

#### Examples

##### Basic Query
Send a standard DNS query for hybecorp.com to Google's DNS server:
```
pada hybecorp.com 8.8.8.8
```

##### Custom Port
Send a DNS query to a non-standard port:
```
pada -p 5353 hybecorp.com localhost
```

##### Specify Transaction ID
Send a DNS query with a specific transaction ID:
```
pada -t 4242 hybecorp.com localhost
```

##### Send as Response
Send a packet formatted as a DNS response rather than a query:
```
pada -r -i 1.2.3.4 hybecorp.com localhost
```

##### Combined Options
Send a custom DNS query with multiple options:
```
pada -p 8053 -t 1337 hybecorp.com localhost
```

#### Anatomy of a DNS Packet
```
+------------------+--------------------+
|         Header (12 bytes)             |
+------------------+--------------------+
| Transaction ID (2 bytes)              |
+------------------+--------------------+
|QR| Opcode |AA|TC|RD|RA|Z|AD|CD| RCODE |
+------------------+--------------------+
| Question Count (2 bytes)              |
+------------------+--------------------+
| Answer Count (2 bytes)                |
+------------------+--------------------+
| Authority Count (2 bytes)             |
+------------------+--------------------+
| Additional Count (2 bytes)            |
+------------------+--------------------+
                   |
+------------------+--------------------+
|      Question Section (Variable)      |
+------------------+--------------------+
| Query Name (Variable)                 |
+------------------+--------------------+
| Query Type (2 bytes)                  |
+------------------+--------------------+
| Query Class (2 bytes)                 |
+------------------+--------------------+
                   |
+------------------+--------------------+
|      Answer Section (Variable)        |
+------------------+--------------------+
| Name (Variable)                       |
+------------------+--------------------+
| Type (2 bytes)                        |
+------------------+--------------------+
| Class (2 bytes)                       |
+------------------+--------------------+
| TTL (4 bytes)                         |
+------------------+--------------------+
| Data Length (2 bytes)                 |
+------------------+--------------------+
| Data (Variable, e.g., A Record)       |
+------------------+--------------------+
                   |
+------------------+--------------------+
|     Authority Section (Variable)      |
+------------------+--------------------+
| Name (Variable)                       |
+------------------+--------------------+
| Type (2 bytes)                        |
+------------------+--------------------+
| Class (2 bytes)                       |
+------------------+--------------------+
| TTL (4 bytes)                         |
+------------------+--------------------+
| Data Length (2 bytes)                 |
+------------------+--------------------+
| Data (Variable, e.g., NS Record)      |
+------------------+--------------------+
                   |
+------------------+--------------------+
|     Additional Section (Variable)     |
+------------------+--------------------+
| Name (Variable)                       |
+------------------+--------------------+
| Type (2 bytes)                        |
+------------------+--------------------+
| Class (2 bytes)                       |
+------------------+--------------------+
| TTL (4 bytes)                         |
+------------------+--------------------+
| Data Length (2 bytes)                 |
+------------------+--------------------+
| Data (Variable, e.g., Extra Info)     |
+------------------+--------------------+
```

## [50 Points] Task 3: Parallel Kaminsky Attack

After analyzing the DNS Server and sending a few test packets with Pada, you think you have discovered a vulnerability to HYBE's DNS Server.

You have noticed that HYBE's server has not implemented source port randomization nor case randomization, and you remember from your time in CSE 508 that this means the server will be vulnerable to a Kaminsky attack! You will use this knowledge to take control of HYBE’s DNS and ensure New Jeans fans reach independent K-Pop outlets instead.

#### How the Attack Works

As you learned in class, the Kaminsky attack is a type of DNS Cache Poisoning attack. It exploits the way DNS resolvers store information by flooding them with fake responses in an attempt to inject malicious data into their cache.

1. The attacker sniffs the IP and Name of the Nameserver (e.g. 1.2.3.4 ns.newjeans.kr).
2. The attacker sends a DNS query for a non-existent subdomain (e.g., kaminsky.newjeans.kr).
3. The attacker then floods the DNS server with spoofed DNS responses.
4. Each fake response contains an additional section that assigns a fake IP address to the authoritative name server (e.g., IP of ns.newjeans.kr => attacker-controlled IP).
5. If the transaction ID in one of the fake responses matches the original request, the poisoned record gets cached.
6. Once cached, the attacker controls DNS resolution for the entire name server for as long as the TTL lasts (pick a big one!).

To make this attack work, you must spoof your source IP to make it appear as if the response is coming from the legitimate name server. This will allow you to take over as the primary name server and manipulate future queries.

### Security Features in Place

Unfortunately for you, HYBE's network security team has briefly studied the Kaminsky attack, and improved their DNS servers with 2 security features to make this attack more difficult. 

1. The transaction ids will be randomized, so you will not have a way to predict the transaction ids ahead of time. 
2. A `per-query` attack detection mechanism has been implemented, and will lock updates for a specific query (e.g. kaminsky.newjeans.kr) if it receives more than 3 responses for it, and return a `Connection Refused` error. 

### Bypassing the Security Measures

Fortunately, HYBE's security team has not taken CSE 508 with Prof. Chowdhury! As a well-read security engineer, you know that per-query detection mechanisms are an insufficient defense against a cache poisoning attack. You realize that instead of flooding responses for a single subdomain, you can spread your attack across multiple fake subdomains. This technique is known as a __Parallel Kaminsky Attack__. In this attack, you send hundreds of fake subdomains with a single fake transaction ID.

This avoids the implemented attack protections while still increasing your chances of guessing the correct transaction ID.

### Modifications to Simplify Your Attack

To make your implementation easier, we have modified the attack scenario as follows:

1. Simple Name Server

There is only one authoritative name server that HYBE uses, which you observed in 1a.

This means that you will only need to poison one name server to control every query, rather than identifying and poisoning multiple nameservers per query.

2. Port-Based Spoofing Instead of Hosting a Public DNS Server

In the additional section when you are overwriting the IP of the nameserver, you may use IP section to specify a port number (ex: IP 1.1.1.1 => port 1111). This means that you will need to set the IP to the local port your nameserver is running on, rather than hosting your own nameserver on some public IP address.

3. Timeout 

The DNS server implements a timeout for responses, so if a valid response is not received within 15 seconds it will stop listening for them. This will prevent the program from hogging your system resources. 

4. Limited Transaction IDs

All Transaction IDs will be within the range of 0-1023. This will make it an order of magnitude faster for you to guess the correct ID.

### Your Task

You must implement a Command Line Interface (CLI) tool that executes a Parallel Kaminsky Attack on HYBE's DNS resolver.

Your program should be able to:
1. Run your own malicious name server
2. Find the nameserver's IP and Name before executing an attack
3. Generate fake subdomain DNS queries to maximize the probability of cache poisoning
4. Spoof DNS responses to inject a malicious name server IP
5. Use the Authority & Additional sections to overwrite the existing name server record with your own
6. Handle randomized transaction IDs and bypass rate-limiting defenses

The CLI tool should exit after the cache has been poisoned.

#### Included Files

`task3/build.sh` - this file will compile your code so that we can run and test it 

`task3/kaminsky` - this will be the name of the executable file generated by `task3/build.sh` for us to run & test

#### Restrictions

You are allowed to use whatever libraries you would like as part of the CLI (e.g. parsing flags and arguments). Scapy in Python and meikg/dns in Go are allowed.

#### Usage
```
kaminsky [OPTIONS] <dns_server> <domain> <ip>
```
A CLI tool to perform a Kaminsky attack by poisoning a DNS cache.

#### Options
- `-p <port>`        Specify the port to send malicious responses to. (default: 53)
- `-n <port>`        Specify the port your name server will run on. (default: 9953)

#### Arguments

- `<dns_server>`  The DNS server to target
- `<domain>`      Domain name to target in the Kaminsky attack.
- `<ip>`          This will be the new IP of the provided domain after the attack finishes executing

#### Example Usage
```
kaminsky -p 53 localhost newjeans.kr 1.2.3.4
# this will posion the cache of domain newjeans.kr to 1.2.3.4 on the dns running on port 53.
```
#### Examples DNS Packets

##### Fake DNS Request
```
════════════════════════════════════════════════
|  Transaction ID  : 0722                      |
════════════════════════════════════════════════
|  QR: false | OpCode: 0 | AA: false           |
|  TC: false | RD: true | RA: false            |
|  Z: false | AD: true | CD: false | RCODE: 0  |
════════════════════════════════════════════════
|  QD Count        : 1                         |
|  AN Count        : 0                         |
|  NS Count        : 0                         |
|  AR Count        : 0                         |
════════════════════════════════════════════════
|  Query Name      : kaminsky.newjeans.kr      |
|  Query Type      : A                        |
|  Query Class     : 1                         |
════════════════════════════════════════════════
|               Answers                        |
════════════════════════════════════════════════
|             Authorities                      |
════════════════════════════════════════════════
|           Additional Records                 |
════════════════════════════════════════════════
```
##### Fake DNS Response
```
════════════════════════════════════════════════
|  Transaction ID  : 0722                      |
════════════════════════════════════════════════
|  QR: true | OpCode: 0 | AA: false            |
|  TC: false | RD: true | RA: true             |
|  Z: false | AD: false | CD: false | RCODE: 0 |
════════════════════════════════════════════════
|  QD Count        : 1                         |
|  AN Count        : 1                         |
|  NS Count        : 1                         |
|  AR Count        : 1                         |
════════════════════════════════════════════════
|  Query Name      : kaminsky.newjeans.kr      |
|  Query Type      : A                         |
|  Query Class     : 1                         |       
════════════════════════════════════════════════
|               Answers                        |
════════════════════════════════════════════════
|  Name: kaminsky.newjeans.kr                  |
|  Type: A                                     |
|  Class: 1                                    |
|  TTL: 256                                    |
|  Data Length: 4                              |
|  Data: 142.250.72.110                        |
════════════════════════════════════════════════
|              Authorities                     |
════════════════════════════════════════════════
|  Name: newjeans.kr                           |
|  Type: NS                                    |
|  Class: 1                                    |
|  TTL: 300                                    |
|  Data Length: 17                             |
|  Data: ns.newjeans.kr                        |
════════════════════════════════════════════════
|          Additional Records                  |
════════════════════════════════════════════════
|  Name: ns.newjeans.kr                        |
|  Type: A                                     |
|  Class: 1                                    |
|  TTL: 33505                                  |
|  Data Length: 4                              |
|  Data: 9.9.9.9 (port 9999)                   |
════════════════════════════════════════════════
```