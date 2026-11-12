
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from datetime import date, timedelta
from pathlib import Path
import sqlite3

app = FastAPI(
    title="Smart Travel Planner",
    description="Smart travel planning without AI",
    version="1.1.0"
)

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "fronted"
DATABASE_PATH = Path(__file__).with_name("travel.db")

# Frontend static files
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TravelRequest(BaseModel):
    destination: str = Field(min_length=2)
    start_date: date
    end_date: date
    budget: float = Field(gt=0)
    travelers: int = Field(ge=1)
    travel_style: str = Field(min_length=2)


ACTIVITIES = {
    "adventure": [
        "Explore famous natural attractions",
        "Try an outdoor adventure activity",
        "Discover hidden places and local landscapes",
        "Enjoy hiking and outdoor exploration",
        "Visit a beautiful viewpoint"
    ],
    "luxury": [
        "Enjoy a relaxing day at a luxury resort",
        "Visit premium restaurants and cafes",
        "Explore exclusive attractions",
        "Enjoy a spa and wellness experience",
        "Discover the city's finest shopping areas"
    ],
    "budget": [
        "Explore free local attractions",
        "Visit local markets and street food areas",
        "Discover historical streets and landmarks",
        "Enjoy affordable local activities",
        "Explore public parks and cultural areas"
    ],
    "culture": [
        "Visit historical landmarks and museums",
        "Discover local traditions and culture",
        "Explore traditional markets",
        "Try authentic local food",
        "Visit cultural and historical attractions"
    ],
    "relaxation": [
        "Enjoy a relaxing day at the beach",
        "Visit a peaceful park or garden",
        "Explore local cafes",
        "Enjoy a wellness activity",
        "Spend time exploring beautiful scenery"
    ]
}


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/plan")
def create_travel_plan(request: TravelRequest):

    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date."
        )

    duration = (request.end_date - request.start_date).days + 1

    if duration > 30:
        raise HTTPException(
            status_code=400,
            detail="For now, trips can be up to 30 days."
        )

    style = request.travel_style.lower().strip()
    activities = ACTIVITIES.get(style, ACTIVITIES["culture"])

    daily_budget = request.budget / duration / request.travelers

    daily_itinerary = []

    for day_number in range(duration):
        current_date = request.start_date + timedelta(days=day_number)
        activity = activities[day_number % len(activities)]

        daily_itinerary.append({
            "day": day_number + 1,
            "date": current_date.isoformat(),
            "title": f"Day {day_number + 1}: Explore {request.destination}",
            "description": activity,
            "activities": [
                activity,
                "Explore local food and restaurants",
                "Enjoy free time and discover the area"
            ]
        })

    return {
        "message": "Travel plan generated successfully!",
        "destination": request.destination,
        "duration": duration,
        "travelers": request.travelers,
        "total_budget": request.budget,
        "daily_budget_per_person": round(daily_budget, 2),
        "travel_style": style,
        "daily_itinerary": daily_itinerary
    }


@app.get("/cities")
def get_cities():
    connection = get_db_connection()

    try:
        cities = connection.execute("""
            SELECT id, name, description
            FROM cities
            ORDER BY name
        """).fetchall()

        return [dict(city) for city in cities]
    finally:
        connection.close()


@app.get("/attractions")
def get_attractions(city: str):
    connection = get_db_connection()

    try:
        attractions = connection.execute("""
            SELECT attractions.id,
                   attractions.name,
                   attractions.category,
                   attractions.description,
                   cities.name AS city
            FROM attractions
            JOIN cities ON attractions.city_id = cities.id
            WHERE cities.name = ?
            ORDER BY attractions.name
        """, (city,)).fetchall()

        return [dict(place) for place in attractions]
    finally:
        connection.close()
