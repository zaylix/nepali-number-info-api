import csv
import json
import random
import re
import os

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nepali Name Components
FIRST_NAMES = ["Ram", "Shyam", "Hari", "Sita", "Gita", "Rita", "Bijay", "Sanjay", "Hemant", "Prakash", "Sunita", "Anita", "Deepak", "Sandesh", "Rohan", "Aayush", "Bishal", "Kiran", "Nabin", "Suman", "Pabitra", "Nirmala", "Kabita", "Rajesh", "Suresh", "Gopal", "Parshu"]
MIDDLE_NAMES = ["Bahadur", "Prasad", "Kumar", "Kumari", "Devi", "Maya", "Raj", "Lal", "Nath", "Singh", "Giri", "Chandra", "Kanta"]
LAST_NAMES = ["Sharma", "Adhikari", "Bhattarai", "Khatri", "Thapa", "Magar", "Gurung", "Rai", "Limbu", "Shrestha", "Maharjan", "Bajracharya", "Pandey", "Paudel", "Gautam", "Basnet", "Yadav", "Shah", "Singh", "Jha", "Khadka", "Mishra", "Acharya", "Dahal", "Koirala", "Oli"]

CITIES = ["Kathmandu", "Pokhara", "Lalitpur", "Bharatpur", "Biratnagar", "Birgunj", "Janakpur", "Ghorahi", "Hetauda", "Dhangadhi", "Itahari", "Dharan", "Butwal", "Nepalgunj", "Bhadrapur", "Damak", "Gulariya", "Tulsipur"]
DISTRICTS = ["Kathmandu", "Kaski", "Lalitpur", "Chitwan", "Morang", "Parsa", "Dhanusa", "Dang", "Makwanpur", "Kailali", "Sunsari", "Rupandehi", "Banke", "Jhapa", "Illam", "Bardiya", "Surkhet"]

# Nepali Address Components
LOCAL_ADDRESS_COMPONENTS = [
    "Ward No. " + str(random.randint(1, 32)),
    "Tole " + str(random.randint(1, 15)),
    "Marg " + str(random.randint(1, 20)),
    "Galli " + str(random.randint(1, 10)),
    "Gaunpalika " + str(random.randint(1, 10)),
    "Nagarplika " + str(random.randint(1, 10))
]

def generate_fake_nepali_data(count=100):
    fake_data = []
    for i in range(count):
        fname_base = random.choice(FIRST_NAMES)
        mname = random.choice(MIDDLE_NAMES) if random.random() < 0.3 else "" # 30% chance of middle name
        lname = random.choice(LAST_NAMES)
        
        fname = f"{fname_base} {mname}".strip() if mname else fname_base
        name = f"{fname} {lname}".strip()

        city = random.choice(CITIES)
        district = random.choice(DISTRICTS)
        
        # Generate a random mobile number (NTC or Ncell or Smart)
        prefix_options = ["984", "985", "986", "974", "975", "980", "981", "982", "961", "962", "988"]
        prefix = random.choice(prefix_options)
        mobile = prefix + "".join([str(random.randint(0, 9)) for _ in range(7)])
        
        address = ""
        if random.random() < 0.8: # 80% chance of having an address
            address_components = [random.choice(LOCAL_ADDRESS_COMPONENTS), city, district, "Nepal"]
            address = ", ".join(filter(None, address_components))
        
        circle = "UNKNOWN"
        if prefix in ["984", "985", "986", "974", "975"]:
            circle = "NTC"
        elif prefix in ["980", "981", "982"]:
            circle = "NCELL"
        elif prefix in ["961", "962", "988"]:
            circle = "SMART"

        entry = {
            "address": address,
            "alt": "",
            "circle": circle,
            "email": f"{fname_base.lower()}.{lname.lower()}{random.randint(10, 99)}@gmail.com" if random.random() < 0.7 else "", # 70% chance of email
            "fname": fname,
            "id": str(random.randint(100000000000, 999999999999)),
            "mobile": mobile,
            "name": name,
            "gender": random.choice(["Male", "Female"]) if random.random() < 0.9 else "", # 90% chance of gender
        }
        
        if random.random() < 0.4: # 40% chance of father's name
            entry["father_name"] = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if random.random() < 0.2: # 20% chance of spouse's name
            entry["spouse_name"] = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if random.random() < 0.15: # 15% chance of Nagrita No.
            entry["nagrita_no"] = "".join([str(random.randint(0, 9)) for _ in range(random.randint(8, 12))])

        fake_data.append(entry)
    return fake_data

def process_csv(file_path):
    data = []
    if not os.path.exists(file_path):
        print(f"CSV file not found at {file_path}. Skipping CSV processing.")
        return data
        
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                phone = row.get('Phone', '').strip()
                # Clean phone number
                phone = re.sub(r'[^0-9]', '', phone)
                if phone.startswith('977'):
                    phone = phone[3:]
                
                if len(phone) == 10:
                    prefix = phone[:3]
                    circle = "UNKNOWN"
                    if prefix in ["984", "985", "986", "974", "975"]:
                        circle = "NTC"
                    elif prefix in ["980", "981", "982"]:
                        circle = "NCELL"
                    elif prefix in ["961", "962", "988"]:
                        circle = "SMART"
                    
                    data.append({
                        "address": f"{row.get('Street addr', '')} {row.get('Locality addr', '')} {row.get('Region Addr', '')}".strip(),
                        "alt": "",
                        "circle": circle,
                        "email": "",
                        "fname": row.get('Given Name', ''),
                        "id": row.get('id', '').split(':')[-1],
                        "mobile": phone,
                        "name": f"{row.get('Given Name', '')} {row.get('Family Name', '')}".strip()
                    })
    except Exception as e:
        print(f"Error processing CSV: {e}")
    return data

if __name__ == "__main__":
    # Use relative path for CSV if it exists in the same repo, otherwise skip
    csv_path = os.path.join(BASE_DIR, "Nepallocatefamily_com2022.05.csv")
    csv_data = process_csv(csv_path)
    
    # Load existing database if it exists to append new data
    db_path = os.path.join(BASE_DIR, "database.json")
    existing_data = []
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            existing_data = json.load(f)
    
    # Generate 700 new fake entries
    new_fake_data = generate_fake_nepali_data(700)
    
    # Combine everything, avoiding duplicates based on mobile number
    seen_mobiles = {entry["mobile"] for entry in existing_data}
    combined_data = existing_data
    
    for entry in csv_data + new_fake_data:
        if entry["mobile"] not in seen_mobiles:
            combined_data.append(entry)
            seen_mobiles.add(entry["mobile"])
    
    with open(db_path, "w") as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"Database updated. Total entries: {len(combined_data)}")
