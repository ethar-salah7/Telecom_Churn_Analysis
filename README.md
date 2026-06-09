#  Telecom Customer Churn Analytics

> A full end-to-end data pipeline and analytics dashboard built to understand **why telecom customers leave** — and what the business can do about it.

---

##  Architecture

<img width="1600" height="877" alt="arch" src="https://github.com/user-attachments/assets/c339b6e0-4381-4909-8332-512decefd226" />


---

##  Pipeline Overview

The project follows the **Medallion Architecture** (Bronze → Silver → Gold), a standard pattern used in production data engineering.

```
Raw CSV
   ↓
 Bronze Layer     — Load raw data as-is, no transformations
   ↓
 EDA              — Explore distributions, nulls, and outliers
   ↓
 Silver Layer     — Data quality & cleaning
   ↓
 Docker           — SQL Server running in an isolated container
   ↓
 Gold Layer       — Star schema data warehouse
   ↓
 Power BI         — Interactive analytics dashboard
```

---

##  Data Quality — Silver Layer

All cleaning logic lives in `silver.py`. Issues addressed:

| Issue | Column(s) | Fix Applied |
|---|---|---|
| Structural nulls | `internet_type`, `online_security`, `streaming_*` | Filled with `"No Internet Service"` |
| Structural nulls | `multiple_lines` | Filled with `"No Phone Service"` |
| Structural nulls | `churn_category`, `churn_reason` | Filled with `"None"` for Stayed/Joined |
| Negative charges | `monthly_charge` | Clipped to `0` |
| Inconsistent reasons | `churn_reason` (20+ values) | Grouped into 4 categories |
| Data type issue | `zip_code` | Cast from int to string |
| Duplicate rows | All columns | `drop_duplicates()` applied |

---

##  Data Warehouse — Star Schema

The Gold layer uses a **Star Schema** stored in SQL Server (`customer_churn_dwh`).

```
                    ┌─────────────────┐
                    │  customer_dim   │
                    └────────┬────────┘
                             │
┌─────────────┐    ┌─────────┴──────────┐    ┌──────────────┐
│ service_dim ├────┤ fact_subscriptions ├────┤ address_dim  │
└─────────────┘    └─────────┬──────────┘    └──────────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
        ┌──────┴──────┐           ┌────────┴───────┐
        │  churn_dim  │           │  payment_dim   │
        └─────────────┘           └────────────────┘
```

**Fact Table:** `fact_subscriptions` — contains all measurable metrics (monthly charge, GB download, referrals, revenue)

**Dimension Tables:**
- `customer_dim` — age, gender, marital status, dependents
- `address_dim` — city, latitude, longitude, zip code
- `service_dim` — internet type, phone service, streaming, security
- `payment_dim` — contract type, payment method, paperless billing
- `churn_dim` — churn category, churn reason

---

##  Key Insights

**1.  New customers are the highest risk**
Customers in their first 12 months have a **47% churn rate** — the business must focus on onboarding and early retention.

**2.  Competition is the #1 churn driver**
841 customers left due to competitor offers — the problem is pricing and promotions, not service quality.

**3.  Contract type is the strongest churn predictor**
- Month-to-Month: ~42% churn rate
- One Year: ~11% churn rate
- Two Year: ~3% churn rate

Converting customers to longer contracts is the single most impactful retention lever.

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Data processing | Python · Pandas |
| Database | SQL Server (Docker) |
| Containerization | Docker |
| Visualization | Power BI |
| Version control | Git · GitHub |

---

##  How to Run

**1. Start SQL Server in Docker**
```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourPassword" \
  -p 1434:1433 --name sql_churn \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

**2. Run the pipeline**
```bash
python bronze.py
python silver.py
```

**3. Open Power BI**
Connect to `localhost,1434` → database `customer_churn_dwh`

---

##  Project Structure

```
telecom-churn/
│
├── bronze.py              # Raw data loader
├── silver.py              # Data quality & cleaning
├── telecom_customer_churn.csv  # Source data
│
├── images/
│   ├── architecture.png
│   ├── churn_overview.png
│   └── churn_deep_dive.png
│
└── README.md
```

---

##  Team
* Ethar Elmahalawy - [GitHub Profile](https://github.com/emahalawy)
* Amira Mohamed - [GitHub Profile](https://github.com/Amiramuhammed)
* Alaa Mahdy - [GitHub Profile](https://github.com/Alaa303)
