import pandas as pd
import gspread
import google.generativeai as genai
from oauth2client.service_account import ServiceAccountCredentials
import re
from googletrans import Translator  

# Google Sheets Setup
SHEET_ID = "15Gdhllj1xU168rBorrQiJ-4yHS84k9-tnx2h5tjjXqc"
SHEET_NAME = "Sheet1"
CREDENTIALS_FILE = "credentials.json"

# Google Gemini API Setup
API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with actual API Key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Translator Setup
translator = Translator()

# Fetch data from Google Sheets
def fetch_google_sheets(sheet_id, sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
        return pd.DataFrame(sheet.get_all_records())
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

# Normalize tenure period
def normalize_tenure(tenure_str):
    if not isinstance(tenure_str, str):
        return (0, 0)

    tenure_str = tenure_str.lower()
    parts = re.split(r'\s*-\s*|\s*to\s*', tenure_str)
    parts = [p.strip() for p in parts if p.strip()]

    def to_days(part):
        num_match = re.search(r'(\d+\.?\d*)', part)
        if not num_match:
            return 0
        num = float(num_match.group(1))
        if 'year' in part: return int(num * 365)
        elif 'month' in part: return int(num * 30)
        else: return int(num)

    if not parts: return (0, 0)
    min_days = to_days(parts[0])
    max_days = to_days(parts[-1]) if len(parts) > 1 else min_days
    return (min(min_days, max_days), max(min_days, max_days))

# Extract tenure days from query
def extract_tenure_from_query(query):
    match = re.search(r'(\d+)\s*-\s*(\d+)\s*(year|month|day)s?', query.lower())
    if match:
        num1, num2, unit = int(match.group(1)), int(match.group(2)), match.group(3)
        if unit.startswith("year"):
            return num1 * 365, num2 * 365
        elif unit.startswith("month"):
            return num1 * 30, num2 * 30
        else:
            return num1, num2
    return None, None  # Default case

# Function to get best senior citizen rates
def get_senior_fd_rates(df, min_days, max_days):
    if df.empty or 'Senior Citizen Rate' not in df.columns:
        return "No data available"

    # Convert rates to float
    df['Senior Citizen Rate'] = df['Senior Citizen Rate'].astype(str).str.replace('%', '').astype(float)
    df[['Min Days', 'Max Days']] = df['Tenure Period'].apply(lambda x: pd.Series(normalize_tenure(x)))

    # Filter data
    filtered = df[(df['Min Days'] >= min_days) & (df['Max Days'] <= max_days)]
    if filtered.empty:
        filtered = df[(df['Min Days'] <= max_days) & (df['Max Days'] >= min_days)]
        if filtered.empty:
            return f"No FD rates found for {min_days}-{max_days} days"

    # Find max rate
    best_bank_row = filtered.loc[filtered['Senior Citizen Rate'].idxmax()]
    best_rate = best_bank_row['Senior Citizen Rate']
    
    # Prepare output
    table = "| Bank                 | Senior Citizen Rate |\n"
    table += "|----------------------|--------------------|\n"
    for _, row in filtered.iterrows():
        table += f"| {row['Bank']} | {row['Senior Citizen Rate']}% |\n"

    table += f"\n**Best Rate:** {best_bank_row['Bank']} offers the highest rate of {best_rate}%."

    return table

# AI Agent to process queries with multilingual support
def run_agent(prompt):
    # Detect language
    detected_lang = translator.detect(prompt).lang

    # Translate to English for processing
    if detected_lang != "en":
        prompt = translator.translate(prompt, src=detected_lang, dest="en").text

    min_days, max_days = extract_tenure_from_query(prompt)

    # If FD-related query, fetch rates
    if "fd rate" in prompt.lower() or "fixed deposit" in prompt.lower() or min_days:
        fd_data = fetch_google_sheets(SHEET_ID, SHEET_NAME)
        if not fd_data.empty and min_days and max_days:
            response = get_senior_fd_rates(fd_data, min_days, max_days)
        else:
            response = "Sorry, I couldn't find the FD rates you are looking for."
    else:
        # General AI response from Gemini
        response = model.generate_content(prompt).text

    # Translate response back to original language
    if detected_lang != "en":
        response = translator.translate(response, src="en", dest=detected_lang).text

    return response

# Main Execution
if __name__ == "__main__":
    query = input("Enter your query: ")
    result = run_agent(query)
    print("\nAI Response:\n", result)
