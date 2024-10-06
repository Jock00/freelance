import requests
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# URL for freelance job listing (update this URL)
url = ""
response = requests.get(url)
data = response.json()
projects = data["result"]["projects"]

# Your cookies and headers
cookies = {}
headers = {}

# Parameters for the API requests
params = {
    'compact': 'true',
    'new_errors': 'true',
    'new_pools': 'true',
}

# Bidder ID (update with your ID)
bidder_id = ''  # Add your bidder ID here
json_data = {
    'project_id': 0,
    'bidder_id': bidder_id,
    'amount': 0,
    'period': 0,
    'milestone_percentage': 100,
    'description': ""
}

# Extra text for proposal generation
extra_text = (
    "Make a proposal for me. It's a freelance job, and I want to convince the "
    "client to pick me. Please avoid placeholders like [your name], [your link], "
    "etc. Just give me a direct response. My name is Alex; do not specify my "
    "email address. Avoid using the customer name; be very generic about it. "
    "Make it a bit more human-like, and it's not an email. It's on a bidding "
    "platform; I don't need the subject. It should be a max of 500 characters, "
    "can be less, and do not put new lines or other text manipulation."
)

# Bid URL template
bid_url_template = (
    "https://www.freelancer.com/api/projects/0.1/projects/{p_id}/bids"
    "?limit=1&bidders%5B%5D={bidder_id}"
)

# Iterate through each project
for project in projects:
    project_id = project["id"]
    bid_url = bid_url_template.format(
        p_id=project_id,
        bidder_id=bidder_id
    ).strip()

    # Check for existing bids
    response = requests.get(bid_url, headers=headers, cookies=cookies)
    data = response.json()

    if data["result"]["bids"]:
        continue  # Skip to the next project if bids exist

    # Construct project URL
    project_url = f"https://www.freelancer.com/projects/{project['seo_url']}"

    # Calculate budget
    min_budget = project["budget"]["minimum"]
    max_budget = project["budget"]["maximum"]
    budget = (
        (min_budget + max_budget) / 2
        if 2 * min_budget > max_budget
        else 2 * min_budget
    )
    period = project["bidperiod"] // 2

    # Prepare JSON data for the bid
    json_data.update({
        "project_id": project_id,
        "amount": budget,
        "period": period
    })

    # Generate proposal description
    text = project["description"]
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": text + extra_text}]
    )
    json_data["description"] = completion.choices[0].message.content

    # Submit the bid
    response = requests.post(
        'https://www.freelancer.com/api/projects/0.1/bids/',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    # Check response status
    if response.status_code == 200:
        print(f"{project_url} bid submitted!")
    else:
        print(f"Error submitting bid for {project_url}: {response.text}")
