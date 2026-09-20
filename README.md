# CityScope

A Flask frontend for a LangChain city research assistant using Groq, Tavily, and OpenWeather.

## Run locally

Create a `.env` file from `.env.example`, add your API keys, then run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000.

## Deploy on Render

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Add `GROQ_API_KEY`, `TAVILY_API_KEY`, and `OPENWEATHER_API_KEY` as environment variables.

Never commit `.env` or API keys to the repository.