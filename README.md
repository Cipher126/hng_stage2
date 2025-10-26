# 🌍 Country Data API

A FastAPI-based service that fetches, processes, and visualizes real-world country and exchange rate data.  
It combines information from the **RESTCountries API** and **ExchangeRate API**, estimates GDP, stores the results in a database, and generates a summary image using **Pillow**.

---

## 🚀 Features

- Fetch and merge live country and exchange rate data.
- Estimate GDP values using population and random multipliers.
- Save and update countries in a MySQL-compatible database.
- Serve endpoints for querying countries by:
  - Region
  - Currency
  - Sorting by GDP (descending)
- Generate a dynamic summary image (`summary.png`) showing:
  - Top 5 countries by GDP (with flags)
  - Total number of countries
  - Last refreshed timestamp

---

## 🧠 Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MySQL (via `aiomysql`)
- **HTTP Client:** httpx
- **Image Generation:** Pillow (PIL)
- **Logging:** Python logging module

---

## 📁 Project Structure

```
    ├── cache/
    | ├── summary.png
    ├── core/
    │ ├── config.py
    │ ├── exception.py
    |
    ├── database/
    | ├── connection.py
    │ ├── model.py
    │
    ├── services/
    │ ├── data_fetcher.py
    │ ├── summary_generator.py
    │
    ├── routes/
    │ ├── countries_routes.py
    | ├── status_route.py
    │
    ├── utils/
    │ └── image_generator.py
    │
    └── main.py
```


---

## ⚙️ Environment Variables

You can configure these in your `.env` or directly inside `core/config.py`:

| Variable | Description |
|-----------|-------------|
| `COUNTRIES_API_URL` | RESTCountries API endpoint |
| `EXCHANGE_API_URL` | Exchange rate API endpoint |
| `MIN_GDP_MULTIPLIER` | Minimum random multiplier for GDP estimation |
| `MAX_GDP_MULTIPLIER` | Maximum random multiplier for GDP estimation |
| `DB_HOST` | Database host |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_NAME` | Database name |

---

## 🧩 Endpoints

### **1. POST `/countries/refresh`**
Fetches fresh data from APIs, saves to DB, and generates `cache/summary.png`.

### **2. GET `/countries`**
Optional query parameters:
- `region`
- `currency`
- `sort=gdp_desc`

### **3. GET `/countries/{name}`**
Returns details for a specific country.

### **4. GET `/countries/status`**
Shows total number of countries and last refreshed timestamp.

### **5. DELETE `/countries/{name}`**
Deletes a country from the database.

### **6. GET `/countries/image`**
Serves the summary image with top 5 GDP countries and stats.

---

## 🧪 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/cipher126/hng_stage2.git
cd hng_stage2
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

🛡️ License

This project is licensed under the MIT License — see LICENSE for details.