import requests

import os

# Your Tomba API key and secret
API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'

# Base URL for Tomba's API
TOMBA_API_URL = 'https://api.tomba.io/v1/domain-search'


# Function to fetch emails for a domain with a limit
def fetch_emails(domain, limit):
    headers = {
        'X-Tomba-Key': API_KEY,
        'X-Tomba-Secret': SECRET_KEY
    }

    params = {
        'domain': domain
    }

    response = requests.get(TOMBA_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        emails = data['data']['emails']
        return emails[:limit]  # Limit the number of emails returned
    else:
        print(
            f"Error fetching emails for {domain}: {response.status_code}, {response.text}")
        return []


# Read domains from an input file
def read_domains(input_file):
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    return domains


# Write the collected emails to a file for each domain
def write_emails_to_file(domain, emails):
    # Create output folder if it doesn't exist
    output_folder = 'output_emails'
    os.makedirs(output_folder, exist_ok=True)

    # Write to a file named after the domain
    output_file = os.path.join(output_folder, f"{domain}.txt")
    with open(output_file, 'w') as file:
        file.write(f"Collected {len(emails)} emails for {domain}:\n")
        for email in emails:
            file.write(f"{email['value']}\n")

    print(f"Saved {len(emails)} emails for {domain} to {output_file}")


# Main function to handle the process
def main(input_file, email_limit):
    domains = read_domains(input_file)

    for domain in domains:
        print(f"Fetching emails for {domain}...")
        emails = fetch_emails(domain, email_limit)
        write_emails_to_file(domain, emails)

    print("Email scraping completed!")


# Configurations
input_file = 'domains.txt'  # File containing the domains
email_limit = 5  # Adjust this value to limit the number of emails collected per domain

# Run the main function
main(input_file, email_limit)
