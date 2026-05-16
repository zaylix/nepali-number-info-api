from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="Nepali Number to Info API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load database using relative path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.json")

def load_database():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
            return []
    return []

# Initial load
database = load_database()

def validate_nepali_number(number: str):
    if not number.isdigit() or len(number) != 10:
        return False, "Invalid length or format"
    
    prefix = number[:3]
    # Updated NTC and Ncell prefixes
    if prefix in ["984", "985", "986", "974", "975", "976", "972"]:
        return True, "NTC"
    elif prefix in ["980", "981", "982"]:
        return True, "NCELL"
    elif prefix in ["961", "962", "988"]:
        return True, "SMART"
    else:
        return False, "Unknown Operator"

@app.get("/")
def read_root():
    return {"message": "Welcome to Nepali Number to Info API", "status": "running"}

@app.get("/api/v1/key={key}/number={number}")
def get_number_info(key: str, number: str):
    if key != "diwazz":
        return {"success": False, "message": "Invalid API Key"}

    is_valid, operator = validate_nepali_number(number)
    
    # Reload database to get latest updates
    current_db = load_database()
    results = [entry for entry in current_db if entry["mobile"] == number]
    
    if not results:
        if is_valid:
            return {
                "data": [
                    {
                        "address": "Information not found in primary database",
                        "alt": "",
                        "circle": operator,
                        "email": "",
                        "fname": "Unknown",
                        "id": "0",
                        "mobile": number,
                        "name": "Unknown User"
                    }
                ],
                "source": "primary",
                "success": True,
                "type": "number"
            }
        else:
            return {"success": False, "message": "Invalid Nepali Number", "type": "number"}

    return {
        "data": results,
        "source": "primary",
        "success": True,
        "type": "number"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
