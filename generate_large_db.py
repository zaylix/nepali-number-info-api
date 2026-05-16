import json
import random
import os

# Load names from the downloaded file
with open("/home/ubuntu/nepali_names.txt", "r") as f:
    ALL_NAMES = [line.strip() for line in f if line.strip()]

SURNAMES = ["Sharma", "Adhikari", "Bhattarai", "Khatri", "Thapa", "Magar", "Gurung", "Rai", "Limbu", "Shrestha", "Maharjan", "Bajracharya", "Pandey", "Paudel", "Gautam", "Basnet", "Yadav", "Shah", "Singh", "Jha", "Khadka", "Mishra", "Acharya", "Dahal", "Koirala", "Oli", "Poudel", "Bhandari", "Lamsal", "Regmi", "Subedi", "Aryal", "Neupane", "Ghimire", "Bastola", "Baniya", "Bohara", "Budhathoki", "Chhetri", "Dhakal", "Karki", "Kunwar", "Lamichhane", "Mainali", "Pant", "Prasai", "Pyakurel", "Rana", "Rimal", "Sapkota", "Silwal", "Upreti", "Wagle"]
MIDDLE_NAMES = ["Bahadur", "Prasad", "Kumar", "Kumari", "Devi", "Maya", "Raj", "Lal", "Nath", "Singh", "Giri", "Chandra", "Kanta", "Man", "Maya", "Sari"]
DISTRICTS = ["Kathmandu", "Kaski", "Lalitpur", "Chitwan", "Morang", "Parsa", "Dhanusa", "Dang", "Makwanpur", "Kailali", "Sunsari", "Rupandehi", "Banke", "Jhapa", "Illam", "Bardiya", "Surkhet", "Baglung", "Gorkha", "Syangja", "Tanahun", "Nawalpur", "Parbat", "Myagdi", "Mustang", "Dolpa", "Mugu", "Humla", "Jumla", "Kalikot", "Dailekh", "Jajarkot", "Salyan", "Pyuthan", "Rolpa", "Rukum", "Gulmi", "Arghakhanchi", "Palpa", "Kapilvastu", "Saptari", "Siraha", "Udayapur", "Okhaldhunga", "Khotang", "Solukhumbu", "Sankhuwasabha", "Bhojpur", "Dhankuta", "Tehrathum", "Panchthar", "Taplejung"]

def generate_entry(mobile):
    fname_base = random.choice(ALL_NAMES)
    mname = random.choice(MIDDLE_NAMES) if random.random() < 0.4 else ""
    lname = random.choice(SURNAMES)
    
    fname = f"{fname_base} {mname}".strip() if mname else fname_base
    name = f"{fname} {lname}".strip()
    
    district = random.choice(DISTRICTS)
    ward = random.randint(1, 32)
    
    prefix = mobile[:3]
    circle = "NTC" if prefix in ["984", "985", "986", "974", "975", "976", "972"] else "NCELL"
    
    entry = {
        "address": f"Ward No. {ward}, {district}, Nepal",
        "alt": "",
        "circle": circle,
        "email": f"{fname_base.lower()}.{lname.lower()}{random.randint(10, 999)}@gmail.com" if random.random() < 0.6 else "",
        "fname": fname,
        "id": str(random.randint(100000000000, 999999999999)),
        "mobile": mobile,
        "name": name,
        "gender": random.choice(["Male", "Female"]) if random.random() < 0.95 else ""
    }
    
    # Advanced data
    if random.random() < 0.5:
        entry["nagrita_no"] = f"{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10000, 99999)}"
        entry["ward_no"] = str(ward)
    
    if random.random() < 0.4:
        entry["father_name"] = f"{random.choice(ALL_NAMES)} {random.choice(SURNAMES)}"
    
    if random.random() < 0.2:
        entry["mother_name"] = f"{random.choice(ALL_NAMES)} {random.choice(SURNAMES)}"

    return entry

def main():
    db_path = "/home/ubuntu/nepali-number-info-api/database.json"
    target_size_mb = 55 # Aim for slightly over 50MB
    
    # Track name counts to limit repeats to 100
    name_counts = {}
    
    data = []
    current_size = 0
    
    # Prefixes for NTC and Ncell
    prefixes = ["984", "985", "986", "974", "975", "976", "980", "981", "982"]
    
    print("Generating data...")
    while current_size < target_size_mb * 1024 * 1024:
        prefix = random.choice(prefixes)
        mobile = prefix + "".join([str(random.randint(0, 9)) for _ in range(7)])
        
        entry = generate_entry(mobile)
        
        # Limit name repeats
        full_name = entry["name"]
        if name_counts.get(full_name, 0) >= 100:
            continue
        
        name_counts[full_name] = name_counts.get(full_name, 0) + 1
        data.append(entry)
        
        # Periodically check size (every 5000 entries)
        if len(data) % 5000 == 0:
            temp_json = json.dumps(data)
            current_size = len(temp_json)
            print(f"Current size: {current_size / (1024*1024):.2f} MB ({len(data)} entries)")

    with open(db_path, "w") as f:
        json.dump(data, f)
    
    print(f"Final database size: {os.path.getsize(db_path) / (1024*1024):.2f} MB")
    print(f"Total entries: {len(data)}")

if __name__ == "__main__":
    main()
