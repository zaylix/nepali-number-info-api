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

# Load database
DB_PATH = "database.json"
if os.path.exists(DB_PATH):
    with open(DB_PATH, "r") as f:
        database = json.load(f)
else:
    database = []

def validate_nepali_number(number: str):
    # Basic validation for Nepali mobile numbers
    # NTC: 984, 985, 986, 974, 975
    # Ncell: 980, 981, 982
    # Smart: 961, 962, 988
    if not number.isdigit() or len(number) != 10:
        return False, "Invalid length or format"
    
    prefix = number[:3]
    if prefix in ["984", "985", "986", "974", "975"]:
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
    # Simple key validation (you can expand this)
    if key != "diwazz":
        return {"success": False, "message": "Invalid API Key"}

    is_valid, operator = validate_nepali_number(number)
    
    # Search in database
    results = [entry for entry in database if entry["mobile"] == number]
    
    if not results:
        # If not found, return a placeholder or fake-looking response if it's a valid number
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
