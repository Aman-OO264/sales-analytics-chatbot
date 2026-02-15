import re
from datetime import datetime

def classify_user_query(user_query):

    user_query = user_query.lower()
    current_year = datetime.now().year

    # -----------------------------
    # Year Detection
    # -----------------------------
    years = re.findall(r"\b20\d{2}\b", user_query)

    if "last year" in user_query:
        years.append(str(current_year - 1))
    if "this year" in user_query:
        years.append(str(current_year))

    # -----------------------------
    # Month Detection
    # -----------------------------
    months = [
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    ]

    month_found = None
    for month in months:
        if month in user_query:
            month_found = month
            break

    # -----------------------------
    # Quarter Detection
    # -----------------------------
    quarter_match = re.search(r"\bq[1-4]\b", user_query)
    quarter = quarter_match.group().upper() if quarter_match else None

    # -----------------------------
    # Top N Detection
    # -----------------------------
    top_match = re.search(r"top\s*(\d+)", user_query)
    top_n = int(top_match.group(1)) if top_match else None

    # Highest Product Detection
    if "highest" in user_query and "product" in user_query:
     return {
        "intent": "ranking",
        "metric": "sales",
        "top_n": 1,
        "category": None,
        "time_filter": years[0] if years else None
    }

    # -----------------------------
    # Category Detection
    # -----------------------------
    categories = ["beverages", "snacks", "dairy", "grocery"]
    category_found = None

    for cat in categories:
        if cat in user_query:
            category_found = cat
            break

    
    # -----------------------------
    # Comparison Intent
    # -----------------------------
    if "compare" in user_query:
     return {
            "intent": "comparison",
            "metric": "sales",
            "time_filter": years if years else None,
            "month": month_found,
            "quarter": quarter
        }

    # -----------------------------
    # Trend Intent
    # -----------------------------
    elif "trend" in user_query:
        return {
            "intent": "trend",
            "metric": "sales",
            "time_filter": years[0] if years else None,
            "month": month_found,
            "quarter": quarter
        }

    # -----------------------------
    # Top N Intent
    # -----------------------------
    elif top_n:
        return {
            "intent": "ranking",
            "metric": "sales",
            "top_n": top_n,
            "category": category_found,
            "time_filter": years[0] if years else None
        }
    
    

    # -----------------------------
    # Customers
    # -----------------------------
    elif "customer" in user_query:
        return {
            "intent": "descriptive",
            "metric": "customers",
            "time_filter": years[0] if years else None
        }
    
    

    # -----------------------------
    # Revenue
    # -----------------------------
    elif "revenue" in user_query:
     return {
        "intent": "descriptive",
        "metric": "revenue",
        "time_filter": years[0] if years else None,
        "month": month_found,
        "quarter": quarter
    }

    

    # -----------------------------
    # Default Sales
    # -----------------------------
    else:
     return {
        "intent": "descriptive",
        "metric": "sales",
        "time_filter": years[0] if years else None,
        "month": month_found,
        "quarter": quarter
    }

    # Simulating GPT behaviour using rule-based logic
    #Not actively calling GPT API (because of quota issue)

    #What I Have Achieved

#I have built a GenAI Layer that:

#✔ Accepts natural language input
#✔ Detects:
#Intent (descriptive / comparison / trend / ranking)
#Metric (sales / revenue / customers)
#Year
#Month
#Quarter#✔ Returns structured JSON output