#Senior-Friendly FD Rate Comparison Assistant

## Overview
Our Model is an AI-powered assistant designed to help senior citizens compare Fixed Deposit (FD) rates easily. The AI agent utilizes Google's Gemini model for answering queries and fetches real-time FD rates from Google Sheets. It supports multilingual queries and responds accordingly.

## Features
- **FD Rate Comparison**: Retrieves and compares FD rates for senior citizens from a Google Sheet.
- **Multilingual Support**: Accepts queries in multiple Indian languages and responds in the same language.
- **Google Gemini Integration**: Uses Google's Gemini model for general queries.
- **Real-Time Data**: Fetches live FD rates from a Google Sheet.
- **User-Friendly Interface**: Provides an intuitive UI with predefined query suggestions.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **AI Model**: Google Gemini
- **Database**: Google Sheets (via gspread)
- **Translation**: Deep Translator

## Installation & Setup
### 1. Clone the Repository
```sh
$ git clone https://github.com/your-repo/Agno-AI.git
$ cd Agno-AI
```
### 2. Install Dependencies
```sh
$ pip install pandas gspread google-generativeai oauth2client deep-translator flask
```
### 3. Configure API Keys
- **Google Sheets API**:
  - Create a `credentials.json` file with your Google Cloud API credentials.
- **Google Gemini API**:
  - Set up your Gemini API key in `config.py`:
    ```python
    API_KEY = "your-gemini-api-key"
    ```

### 4. Run the Backend
```sh
$ python app.py
```

### 5. Open the Frontend
- Open `index.html` in your browser or deploy it on a local server.

## How It Works
1. **User enters a query** (e.g., "Best FD rate for 1-2 years").
2. **Agno AI detects if it's an FD-related query**.
   - If yes, it fetches rates from Google Sheets.
   - If no, it uses Gemini AI to generate a response.
3. **Multilingual Support**:
   - If the query is not in English, it's translated into English before processing.
   - The response is then translated back into the original query language.
4. **The AI displays the answer in a structured format**.

## Example Queries
- "What is the best senior citizen FD rate for 1-2 years?"
- "1-2 saal ke liye sabse achha FD rate kya hai?" (Hindi)
- "1-2 વર્ષ માટે શ્રેષ્ઠ FD દર શું છે?" (Gujarati)

## Future Enhancements
- Voice Query Support
- Mobile App Integration
- Additional Investment Options

## Contributing
Feel free to submit issues or pull requests to improve Agno AI!

## License
This project is licensed under the MIT License.

---
**Author:**   Terracodex
**Contact:** sri09soumya@gmail.com

