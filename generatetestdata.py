import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import names  # Install with: pip install names

# -----------------------------
# Step 1: Generate Account Data
# -----------------------------

# Number of accounts to generate
num_accounts = 800

# Account numbers starting at 10000
account_numbers = list(range(10000, 10000 + num_accounts))

# Possible account types
account_types = ['Active Summer', 'Gold Pass', 'August Pass (Waitlist)',
 'August Pass (Non Member)', 'Offered Membership', 'August Pass (Member)',
 'Waitlist', 'Honorary Pass']

# Possible tags (some accounts may have multiple tags)
possible_tags = ['Gold Pass Eligible', 'Extended Membership']

# Possible site access options
site_access_options = ['1']

# Possible payment statuses
payment_statuses = ['paid', 'unpaid']

# Possible states
states = ['VA', 'DC', 'MD']

# CSV headers for accounts
account_headers = [
    'Acct #', 'Acct Type', 'Tags', 'Date Registered', 'Legacy Acct #', 'User Name',
    'First Name', 'Last Name', 'Email', 'Site Access', 'Directory', 'Guest Credits',
    'Billing Member Email', 'Street Address', 'Street Address 2', 'City', 'State', 'Zip',
    'Cell Phone', 'Work Phone', 'Home Phone', 'Payment Status', 'Checkin Note', '# Members',
    'Authnet', 'Account', 'Member Names'
]

# Initialize a list to hold account data
accounts_data = []

# Dictionary to hold account ID to member names mapping
acct_id_to_member_names = {}

# List to store account IDs for visit generation
account_ids_list = []

for acct_num in account_numbers:
    # Account details
    acct_type = random.choice(account_types)
    
    # Randomly assign tags (0 to 2 tags per account)
    num_tags = random.randint(0, 2)
    tags = random.sample(possible_tags, num_tags)
    tags_str = ', '.join(tags) if tags else ''
    
    # Random registration date in the past year
    date_registered = datetime.now() - timedelta(days=random.randint(0, 365))
    date_registered_str = date_registered.strftime('%Y-%m-%d')
    
    # Legacy account number (simulate with random numbers or leave blank)
    legacy_acct_num = random.choice(['', str(random.randint(1000, 9999))])
    
    # User information
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    user_name = (first_name[0] + last_name).lower()
    email = f"{user_name}@example.com"
    billing_email = email  # Assuming billing email is the same
    
    # Site access
    site_access = random.choice(site_access_options)
    
    # Directory (Yes/No)
    directory = random.choice(['Yes', 'No'])
    
    # Guest credits (0 to 10)
    guest_credits = random.randint(0, 10)
    
    # Address
    street_address = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak St', 'Pine St', 'Maple Ave', 'Cedar Rd'])}"
    street_address_2 = ''
    city = names.get_last_name() + ' City'
    state = random.choice(states)
    zip_code = str(random.randint(10000, 99999))
    
    # Phone numbers
    cell_phone = f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    work_phone = f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    home_phone = f"({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    # Payment status
    payment_status = random.choice(payment_statuses)
    
    # Checkin note (leave blank or add a random note)
    checkin_note = random.choice(['', 'Requires ID', 'VIP Member', ''])
    
    # Number of members (1 to 6)
    num_members = random.randint(1, 6)
    
    # Authnet (simulate with random numbers or IDs)
    authnet = random.choice(['', str(random.randint(100000, 999999))])
    
    # Account (could be same as Acct # or simulate)
    account = str(acct_num)
    
    # Member Names (comma-separated list of members)
    member_names_list = [f"{names.get_first_name()} {names.get_last_name()}" for _ in range(num_members)]
    member_names = ', '.join(member_names_list)
    
    # Store member names for visit generation
    acct_id_to_member_names[acct_num] = member_names_list
    
    # Assemble account data
    account_data = [
        acct_num, acct_type, tags_str, date_registered_str, legacy_acct_num, user_name,
        first_name, last_name, email, site_access, directory, guest_credits,
        billing_email, street_address, street_address_2, city, state, zip_code,
        cell_phone, work_phone, home_phone, payment_status, checkin_note, num_members,
        authnet, account, member_names
    ]
    
    accounts_data.append(account_data)
    
    # Add account ID to list for visit generation
    account_ids_list.append(acct_num)

# Create DataFrame for accounts
accounts_df = pd.DataFrame(accounts_data, columns=account_headers)

# Save accounts to CSV
accounts_df.to_csv('~/data/test/accounts.csv', index=False)

print("Account data generation complete. 'accounts.csv' has been created.")

# ----------------------------------------
# Step 2: Generate Pool Visit Data
# ----------------------------------------

# Define the date range: Memorial Day to Labor Day
start_date = datetime(2024, 5, 25)  # Saturday before Memorial Day 2024
end_date = datetime(2024, 9, 2)     # Labor Day 2024

# Pool operating hours: 10 AM to 9 PM
pool_open_time = 10  # 10 AM
pool_close_time = 21 # 9 PM

# Total number of entries to generate
total_entries = 5000

# Generate a list of dates between start_date and end_date
date_range = pd.date_range(start=start_date, end=end_date)

# Possible member types
member_types = ['Adult', 'Child', 'Guest Pass']

# Possible types (Member or Guest)
types = ['member', 'guest']

# CSV headers for visits
visit_headers = [
    'checkin_time', 'acct_id', 'account_type', 'name', 'member_type', 'type', 'num_credits'
]

# Initialize a list to hold visit data
visits_data = []

# Parameters for binomial distribution
max_visits_per_account = 150
n_trials = max_visits_per_account
# Set an average number of visits per account, e.g., mean_visits = 50
# Solve for p in binomial distribution: mean_visits = n * p
mean_visits = 50
p_success = mean_visits / n_trials  # Probability of a visit on each trial

# Generate number of visits per account using binomial distribution
np.random.seed(42)  # For reproducibility
visits_per_account = np.random.binomial(n=n_trials, p=p_success, size=num_accounts)

# Map account IDs to number of visits
acct_visits_dict = dict(zip(account_ids_list, visits_per_account))


# Function to generate check-in times with higher frequency on Friday evenings and weekends
def generate_checkin_times(num_visits):
    checkin_times = []
    for _ in range(num_visits):
        # Randomly select a date, weighting weekends and Fridays higher
        date = random.choices(
            date_range,
            weights=[3 if d.weekday() >= 5 else 2 if d.weekday() == 4 else 1 for d in date_range]
        )[0]
        
        # Generate a random time between pool opening and closing hours
        # Increase probability for peak hours on Friday evenings and weekends
        if date.weekday() >= 5 or date.weekday() == 4:
            # Weekend or Friday
            peak_hours = list(range(16, 21))  # 4 PM to 9 PM
            non_peak_hours = list(range(pool_open_time, 16))
            hour_weights = [3]*len(peak_hours) + [1]*len(non_peak_hours)
            hours = peak_hours + non_peak_hours
            hour = random.choices(hours, weights=hour_weights)[0]
        else:
            # Weekday
            hour = random.randint(pool_open_time, pool_close_time - 1)
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        checkin_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour, minutes=minute, seconds=second)
        checkin_times.append(checkin_time)
    return checkin_times

# Generate visits per account
for acct_num in account_ids_list:
    num_visits = acct_visits_dict[acct_num]
    if num_visits == 0:
        continue  # Skip accounts with zero visits
    acct_row = accounts_df[accounts_df['Acct #'] == acct_num].iloc[0]
    account_type = acct_row['Acct Type']
    member_names_list = acct_id_to_member_names[acct_num]
    
    # Generate check-in times for the number of visits
    checkin_times = generate_checkin_times(num_visits)
    
    for checkin_time in checkin_times:
        # Randomly select a member from the account
        name = random.choice(member_names_list)
        
        # Randomly assign member type
        member_type = random.choice(member_types)
        
        # Randomly assign type (Member or Guest)
        visit_type = random.choice(types)
        
        # Randomly assign num_credits (assuming it's the number of credits used per visit)
        num_credits = random.randint(1, 5)
        
        # Assemble visit data
        visit_data = [
            checkin_time, acct_num, account_type, name, member_type, visit_type, num_credits
        ]
        
        visits_data.append(visit_data)

# Create DataFrame for visits
visits_df = pd.DataFrame(visits_data, columns=visit_headers)

# Sort by checkin_time
visits_df = visits_df.sort_values('checkin_time').reset_index(drop=True)

# Save visits to CSV
visits_df.to_csv('~/data/test/pool_visits.csv', index=False)

print("Visit data generation complete. 'pool_visits.csv' has been created.")

# Additional: Display some statistics
total_visits_generated = len(visits_df)
print(f"Total visits generated: {total_visits_generated}")

