from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
from pymongo import MongoClient
import uuid

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/wedding_planner')
client = MongoClient(MONGO_URL)
db = client.get_database()

# Collections
wedding_plans_collection = db.wedding_plans
venues_collection = db.venues
cuisine_options_collection = db.cuisine_options
service_categories_collection = db.service_categories

# Models
class VenueOption(BaseModel):
    id: str
    name: str
    description: str
    price_range: str
    capacity: str
    price: int
    image: str
    amenities: List[str]

class CuisineOption(BaseModel):
    id: str
    name: str
    description: str
    price_per_plate: int
    cuisine_type: str
    popular_dishes: List[str]

class ServiceItem(BaseModel):
    id: str
    category: str
    name: str
    description: str
    price: int
    package_type: str

class WeddingPlanItem(BaseModel):
    item_type: str
    item_id: str
    name: str
    price: int
    quantity: Optional[int] = 1

class WeddingPlan(BaseModel):
    plan_id: Optional[str] = None
    guest_count: int
    total_budget: int
    venue: Optional[Dict] = None
    cuisine: Optional[List[Dict]] = None
    services: Optional[List[Dict]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class BudgetCalculation(BaseModel):
    guest_count: int
    venue_id: Optional[str] = None
    cuisine_ids: Optional[List[str]] = None
    service_ids: Optional[List[str]] = None

# Initialize database with sample data
def initialize_database():
    # Clear existing data
    venues_collection.delete_many({})
    cuisine_options_collection.delete_many({})
    service_categories_collection.delete_many({})
    
    # Insert venue options
    venues = [
        {
            "id": "v1",
            "name": "Garden Paradise",
            "description": "Beautiful outdoor garden venue with natural ambiance",
            "price_range": "Budget-Friendly",
            "capacity": "200-300 guests",
            "price": 150000,
            "image": "https://images.unsplash.com/photo-1519167758481-83f29da8c8d6?w=800",
            "amenities": ["Open Garden", "Parking", "Basic Lighting", "Mandap Setup"]
        },
        {
            "id": "v2",
            "name": "Royal Banquet Hall",
            "description": "Elegant indoor banquet hall with AC and modern facilities",
            "price_range": "Mid-Range",
            "capacity": "300-500 guests",
            "price": 300000,
            "image": "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800",
            "amenities": ["AC Hall", "Valet Parking", "Premium Lighting", "Stage Setup", "Green Rooms"]
        },
        {
            "id": "v3",
            "name": "Heritage Palace",
            "description": "Luxurious heritage property with traditional architecture",
            "price_range": "Premium",
            "capacity": "500+ guests",
            "price": 500000,
            "image": "https://images.unsplash.com/photo-1478146896981-b80fe463b330?w=800",
            "amenities": ["Multiple Halls", "Premium Decor", "Valet Service", "Bridal Suite", "Photography Areas"]
        },
        {
            "id": "v4",
            "name": "Lakeside Resort",
            "description": "Scenic lakeside venue perfect for destination weddings",
            "price_range": "Mid-Range",
            "capacity": "150-250 guests",
            "price": 250000,
            "image": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800",
            "amenities": ["Lake View", "Accommodation", "Outdoor Setup", "Bonfire Area"]
        }
    ]
    venues_collection.insert_many(venues)
    
    # Insert cuisine options
    cuisines = [
        {
            "id": "c1",
            "name": "Traditional North Indian",
            "description": "Classic North Indian vegetarian menu",
            "price_per_plate": 400,
            "cuisine_type": "Vegetarian",
            "popular_dishes": ["Dal Makhani", "Paneer Butter Masala", "Naan", "Biryani", "Gulab Jamun"]
        },
        {
            "id": "c2",
            "name": "South Indian Delights",
            "description": "Authentic South Indian vegetarian spread",
            "price_per_plate": 350,
            "cuisine_type": "Vegetarian",
            "popular_dishes": ["Dosa", "Idli", "Sambar", "Rasam", "Payasam"]
        },
        {
            "id": "c3",
            "name": "Mixed Cuisine Buffet",
            "description": "Multi-cuisine buffet with veg and non-veg options",
            "price_per_plate": 600,
            "cuisine_type": "Mixed",
            "popular_dishes": ["Tandoori Chicken", "Mutton Curry", "Paneer Tikka", "Pasta", "Chinese"]
        },
        {
            "id": "c4",
            "name": "Premium Royal Feast",
            "description": "Elaborate royal menu with premium ingredients",
            "price_per_plate": 800,
            "cuisine_type": "Premium",
            "popular_dishes": ["Raan", "Kebabs", "Live Counters", "Continental", "Exotic Desserts"]
        },
        {
            "id": "c5",
            "name": "Simple Vegetarian",
            "description": "Budget-friendly simple veg menu",
            "price_per_plate": 250,
            "cuisine_type": "Vegetarian",
            "popular_dishes": ["Dal", "Sabzi", "Roti", "Rice", "Sweet"]
        }
    ]
    cuisine_options_collection.insert_many(cuisines)
    
    # Insert service categories
    services = [
        {
            "id": "s1",
            "category": "Photography",
            "name": "Basic Photography Package",
            "description": "One photographer for 6 hours",
            "price": 30000,
            "package_type": "Basic"
        },
        {
            "id": "s2",
            "category": "Photography",
            "name": "Premium Photo + Video",
            "description": "Photography + Videography + Drone shots",
            "price": 80000,
            "package_type": "Premium"
        },
        {
            "id": "s3",
            "category": "Decorations",
            "name": "Simple Floral Decor",
            "description": "Basic floral decoration for venue",
            "price": 40000,
            "package_type": "Basic"
        },
        {
            "id": "s4",
            "category": "Decorations",
            "name": "Grand Theme Decor",
            "description": "Themed decoration with lights and props",
            "price": 100000,
            "package_type": "Premium"
        },
        {
            "id": "s5",
            "category": "Entertainment",
            "name": "DJ + Sound System",
            "description": "Professional DJ with sound system",
            "price": 25000,
            "package_type": "Standard"
        },
        {
            "id": "s6",
            "category": "Entertainment",
            "name": "Live Band Performance",
            "description": "Live music band for 3 hours",
            "price": 50000,
            "package_type": "Premium"
        },
        {
            "id": "s7",
            "category": "Makeup",
            "name": "Bridal Makeup Package",
            "description": "Professional bridal makeup + trial",
            "price": 20000,
            "package_type": "Standard"
        },
        {
            "id": "s8",
            "category": "Makeup",
            "name": "Bridal + Family Makeup",
            "description": "Bridal makeup + 5 family members",
            "price": 40000,
            "package_type": "Premium"
        },
        {
            "id": "s9",
            "category": "Invitations",
            "name": "Printed Wedding Cards",
            "description": "Designer printed cards (500 pcs)",
            "price": 15000,
            "package_type": "Standard"
        },
        {
            "id": "s10",
            "category": "Invitations",
            "name": "Premium Digital + Print",
            "description": "Digital invites + premium printed cards",
            "price": 30000,
            "package_type": "Premium"
        },
        {
            "id": "s11",
            "category": "Transportation",
            "name": "Wedding Car Rental",
            "description": "Luxury car for bride/groom",
            "price": 15000,
            "package_type": "Standard"
        },
        {
            "id": "s12",
            "category": "Mehendi",
            "name": "Mehendi Artist",
            "description": "Professional mehendi for bride + family",
            "price": 10000,
            "package_type": "Standard"
        }
    ]
    service_categories_collection.insert_many(services)

# Initialize on startup
initialize_database()

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Wedding Planner API is running"}

@app.get("/api/venues")
def get_venues():
    venues = list(venues_collection.find({}, {"_id": 0}))
    return {"venues": venues}

@app.get("/api/cuisine-options")
def get_cuisine_options():
    cuisines = list(cuisine_options_collection.find({}, {"_id": 0}))
    return {"cuisines": cuisines}

@app.get("/api/services")
def get_services():
    services = list(service_categories_collection.find({}, {"_id": 0}))
    # Group by category
    grouped = {}
    for service in services:
        category = service["category"]
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(service)
    return {"services": grouped, "all_services": services}

@app.post("/api/calculate-budget")
def calculate_budget(calculation: BudgetCalculation):
    total = 0
    breakdown = []
    
    # Add venue cost
    if calculation.venue_id:
        venue = venues_collection.find_one({"id": calculation.venue_id}, {"_id": 0})
        if venue:
            total += venue["price"]
            breakdown.append({
                "category": "Venue",
                "item": venue["name"],
                "cost": venue["price"]
            })
    
    # Add cuisine cost
    cuisine_total = 0
    if calculation.cuisine_ids:
        for cuisine_id in calculation.cuisine_ids:
            cuisine = cuisine_options_collection.find_one({"id": cuisine_id}, {"_id": 0})
            if cuisine:
                cuisine_cost = cuisine["price_per_plate"] * calculation.guest_count
                cuisine_total += cuisine_cost
                breakdown.append({
                    "category": "Catering",
                    "item": cuisine["name"],
                    "cost": cuisine_cost,
                    "details": f"{calculation.guest_count} guests × ₹{cuisine['price_per_plate']}"
                })
    total += cuisine_total
    
    # Add services cost
    if calculation.service_ids:
        for service_id in calculation.service_ids:
            service = service_categories_collection.find_one({"id": service_id}, {"_id": 0})
            if service:
                total += service["price"]
                breakdown.append({
                    "category": service["category"],
                    "item": service["name"],
                    "cost": service["price"]
                })
    
    return {
        "total_cost": total,
        "breakdown": breakdown,
        "guest_count": calculation.guest_count
    }

@app.post("/api/wedding-plan")
def save_wedding_plan(plan: WeddingPlan):
    plan_id = plan.plan_id or str(uuid.uuid4())
    plan_data = plan.dict()
    plan_data["plan_id"] = plan_id
    plan_data["updated_at"] = datetime.now().isoformat()
    
    if not plan.created_at:
        plan_data["created_at"] = datetime.now().isoformat()
    
    wedding_plans_collection.update_one(
        {"plan_id": plan_id},
        {"$set": plan_data},
        upsert=True
    )
    
    return {"message": "Wedding plan saved successfully", "plan_id": plan_id}

@app.get("/api/wedding-plan/{plan_id}")
def get_wedding_plan(plan_id: str):
    plan = wedding_plans_collection.find_one({"plan_id": plan_id}, {"_id": 0})
    if not plan:
        raise HTTPException(status_code=404, detail="Wedding plan not found")
    return plan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
