AI Assistant
A simple chat app. Type or record your voice, and the AI replies in text and voice.
Run on your computer
Get a free API key at https://console.groq.com
Put it in the .env file:

GROQ_API_KEY=your_key_here

Install and start:

pip install -r requirements.txt

streamlit run python.py

Open http://localhost:8501
Put it online (Render)
Upload python.py and requirements.txt to GitHub. Do not upload .env.
On render.com, create a Web Service from that repository.
Build command: pip install -r requirements.txt
Start command: streamlit run python.py --server.port $PORT --server.address 0.0.0.0
Add the environment variable GROQ_API_KEY with your key.
Note
Never share your API key or upload .env.
