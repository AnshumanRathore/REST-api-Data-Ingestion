# REST API Data Ingestion Pipeline ⚙️

An automated pipeline that fetches live JSON data from a public REST API, processes it, and stores it in a relational database.

## 🚀 How It Works
1. **Fetch:** Utilizes the `requests` library to call the Codeforces REST API, handling timeouts and HTTP status errors gracefully.
2. **Process:** Parses the deeply nested JSON response into a `pandas` DataFrame. Filters out irrelevant data, standardizes data types, and transforms metrics (e.g., converting raw seconds into readable hour formats).
3. **Store:** Connects to a `MySQL` database via `SQLAlchemy` to automatically generate the schema and load the transformed records for downstream analytics.

## 🛠️ Tech Stack
* **Language:** Python
* **API Integration:** `requests`
* **Data Processing:** JSON, Pandas
* **Database:** MySQL, SQLAlchemy

## 💡 The Pitch
*"I built a data ingestion system that fetches live competitive programming data from a REST API. I wrote a Python script to handle the HTTP requests, parsed and flattened the complex JSON response, applied transformations using Pandas, and finally loaded the structured data into a MySQL database. It demonstrates a complete end-to-end flow of acquiring and structuring third-party data."*