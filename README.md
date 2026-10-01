# Business Listings Dashboard

A full-stack dashboard that collects business listings, stores them in MySQL, and shows aggregated reports as charts.

## Tech Stack
- Frontend: React (Vite), Recharts, Axios
- Backend: FastAPI (Python), SQLAlchemy, PyMySQL
- Database: MySQL 8
- Scraping: Python, Requests, Pandas

## Project Structure
```
business-dashboard/
├── backend/    FastAPI app (main.py, database.py)
├── frontend/   React dashboard
├── scraper/    scrape.py, add_kochi.py, load_data.py, add_sample.py, data.csv
├── database/   schema.sql, listing_master.sql (full dump)
└── README.md
```

## Data Collection Approach
- Main source: the OpenStreetMap Overpass API, a free and open data source. I chose it because Google Maps and Justdial block scraping and their terms of service forbid it.
- Cities: Kochi, Bangalore, Chennai, Mumbai, Delhi, Hyderabad (up to 150 listings each).
- Categories: Restaurant, Pharmacy, Bank, Cafe, Hospital, School.
- Cleaning: removed rows without a name, removed duplicates, kept only the first phone number, filled missing phone numbers with NULL.
- **Sample data:** 100 of the 1000 listings are mock data, labelled `Sample Data` in the source column. I added them so the source report has more than one source, as the assignment allows. They are not real businesses.

## Setup Instructions

### 1. Database
1. Install MySQL 8.
2. Run `database/schema.sql` to create the database and table, or import `database/listing_master.sql` to get the data too.

### 2. Backend
```
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pymysql cryptography python-dotenv pandas requests
```
Create `backend/.env`:
```
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=business_db
```
Start the API:
```
cd backend
python -m uvicorn main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### 3. Load the data (only if you did not import the dump)
```
python scraper/load_data.py
python scraper/add_sample.py
```
Run each script only once, or rows will be duplicated.

### 4. Frontend
```
cd frontend
npm install
npm run dev
```
Dashboard: http://localhost:5173

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /listings/bulk | Bulk insert listings |
| GET | /dashboard/city-count | Business count per city |
| GET | /dashboard/category-count | Business count per category |
| GET | /dashboard/source-count | Business count per source |

## Challenges Faced
- The Overpass servers returned 504 timeouts. I reduced the search area and added fallback servers with retries.
- Kochi failed in the first run, so I wrote a retry script (`add_kochi.py`) for it.
- Some OpenStreetMap phone fields held several numbers and caused a "Data too long" error. I widened the column to VARCHAR(255) and kept only the first number.
- A bulk insert partly ran and created duplicates. I truncated the table and reloaded it once.
- Many OpenStreetMap entries have no phone or full address, so those fields are NULL or marked "Address not available".
- Google Maps and Justdial could not be scraped within their terms of service, so I used OpenStreetMap plus labelled sample data.