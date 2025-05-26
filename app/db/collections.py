from app.db.mongo import db

webpages_collection = db["webpages"]
scrapping_requests_collection = db["scrapping_requests"]
agents_collection = db["agents"]  # ✅ Add this line
