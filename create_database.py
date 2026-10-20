
import sqlite3
from pathlib import Path
from datetime import datetime

# ==========================================================
# DATABASE: hospital.db
# TABLE:    ED_Metrics
# VIEW:     vw_ED_LiveMetrics
#
# PURPOSE:
# Create dummy hospital ED metrics for the Python dashboard.
# All data is fictional.
# ==========================================================

DB_PATH = Path(__file__).parent / "hospital.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================================================
# STEP 1: DROP EXISTING VIEW AND TABLE
# ==========================================================

cursor.execute("DROP VIEW IF EXISTS vw_ED_LiveMetrics")
cursor.execute("DROP TABLE IF EXISTS ED_Metrics")

# ==========================================================
# STEP 2: CREATE SQL TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE ED_Metrics
(
    Hospital            TEXT PRIMARY KEY,
    EDPatients          INTEGER,
    Waiting             INTEGER,
    Admitted            INTEGER,
    PIAHours            REAL,
    OccupancyPercentage REAL,
    LastUpdated         TEXT
)
""")

# ==========================================================
# STEP 3: INSERT DUMMY DATA
# ==========================================================

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.executemany("""
INSERT INTO ED_Metrics
(
    Hospital,
    EDPatients,
    Waiting,
    Admitted,
    PIAHours,
    OccupancyPercentage,
    LastUpdated
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ("BCH", 145, 48, 32, 3.2, 92.5, now),
    ("EGH", 98, 27, 21, 2.1, 85.3, now),
    ("PMC", 76, 19, 12, 1.8, 78.4, now)
])

# ==========================================================
# STEP 4: CREATE SQL VIEW
# ==========================================================

cursor.execute("""
CREATE VIEW vw_ED_LiveMetrics AS
SELECT
    Hospital,
    EDPatients,
    Waiting,
    Admitted,
    PIAHours,
    OccupancyPercentage,
    LastUpdated
FROM ED_Metrics
""")

conn.commit()

# ==========================================================
# STEP 5: VALIDATE SQL VIEW
# ==========================================================

cursor.execute("""
SELECT *
FROM vw_ED_LiveMetrics
ORDER BY Hospital
""")

rows = cursor.fetchall()

print("\nSQL TABLE AND VIEW CREATED SUCCESSFULLY!")
print("=" * 85)

for row in rows:
    print(row)

print("=" * 85)
print("Database: hospital.db")
print("Table: ED_Metrics")
print("View: vw_ED_LiveMetrics")

conn.close()
