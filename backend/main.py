from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

app = FastAPI(title="Business Listings API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Listing(BaseModel):
    business_name: str
    category: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/listings/bulk")
def insert_listings(listings: List[Listing], db: Session = Depends(get_db)):
    rows = [item.model_dump() for item in listings]
    db.execute(
        text(
            "INSERT INTO listing_master "
            "(business_name, category, city, address, phone, source) "
            "VALUES (:business_name, :category, :city, :address, :phone, :source)"
        ),
        rows,
    )
    db.commit()
    return {"inserted": len(rows)}


def count_by(column: str, db: Session):
    result = db.execute(
        text(
            f"SELECT {column} AS name, COUNT(*) AS count "
            f"FROM listing_master GROUP BY {column} ORDER BY count DESC"
        )
    )
    return [{"name": row.name, "count": row.count} for row in result]


@app.get("/dashboard/city-count")
def city_count(db: Session = Depends(get_db)):
    return count_by("city", db)


@app.get("/dashboard/category-count")
def category_count(db: Session = Depends(get_db)):
    return count_by("category", db)


@app.get("/dashboard/source-count")
def source_count(db: Session = Depends(get_db)):
    return count_by("source", db)