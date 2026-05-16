import csv
import json
import random
import re

# Nepali Name Components
FIRST_NAMES = ["Ram", "Shyam", "Hari", "Sita", "Gita", "Rita", "Bijay", "Sanjay", "Hemant", "Prakash", "Sunita", "Anita", "Deepak", "Sandesh", "Rohan", "Aayush", "Bishal", "Kiran", "Nabin", "Suman"]
LAST_NAMES = ["Sharma", "Adhikari", "Bhattarai", "Khatri", "Thapa", "Magar", "Gurung", "Rai", "Limbu", "Shrestha", "Maharjan", "Bajracharya", "Pandey", "Paudel", "Gautam", "Basnet", "Yadav", "Shah", "Singh", "Jha"]
CITIES = ["Kathmandu", "Pokhara", "Lalitpur", "Bharatpur", "Biratnagar", "Birgunj", "Janakpur", "Ghorahi", "Hetauda", "Dhangadhi", "Itahari", "Dharan", "Butwal", "Nepalgunj"]
DISTRICTS = ["Kathmandu", "Kaski", "Lalitpur", "Chitwan", "Morang", "Parsa", "Dhanusa", "Dang", "Makwanpur", "Kailali", "Sunsari", "Rupandehi", "Banke"]

def generate_fake_nepali_data(count=100):
    fake_data = []
    for i in range(count):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        name = f"{fname} {lname}"
        city = random.choice(CITIES)
        district = random.choice(DISTRICTS)
        
        # Generate a random mobile number (NTC or Ncell)
        prefix = random.choice(["984", "985", "986", "980", "981", "982"])
        mobile = prefix + "".join([str(random.randint(0, 9)) for _ in range(7)])
        
        address = f"{random.choice(['Ward No. ' + str(random.randint(1, 32)), 'Tole ' + str(random.randint(1, 10))])}, {city}, {district}, Nepal"
        
        circle = "NTC" if prefix in ["984", "985", "986"] else "NCELL"
        
        fake_data.append({
            "address": address,
            "alt": "",
            "circle": circle,
            "email": f"{fname.lower()}.{lname.lower()}{random.randint(10, 99)}@gmail.com",
            "fname": fname,
            "id": str(random.randint(100000000000, 999999999999)),
            "mobile": mobile,
            "name": name
        })
    return fake_data

def process_csv(file_path):
    data = []
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
                    if prefix in ["984", "985", "986"]:
                        circle = "NTC"
                    elif prefix in ["980", "981", "982"]:
                        circle = "NCELL"
                    
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
    csv_data = process_csv("/home/ubuntu/upload/Nepallocatefamily_com2022.05.csv")
    fake_data = generate_fake_nepali_data(200)
    
    combined_data = csv_data + fake_data
    
    with open("database.json", "w") as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"Database created with {len(combined_data)} entries.")
