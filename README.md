# AI Voice Assistant

An AI-powered voice assistant built using Python and Streamlit. Users can type messages or record their voice, and the assistant responds with AI-generated text and voice.

## Features

- Text-based AI conversations
- Voice input and recording
- AI-generated responses
- Text-to-speech voice output
- Simple and interactive Streamlit interface
- Groq API integration
- Easy local setup and deployment

## Technologies Used

- Python
- Streamlit
- Groq API
- Speech Recognition
- Text-to-Speech

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd voice_assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Get your free API key from [Groq Console](https://console.groq.com).

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Application

```bash
streamlit run python.py
```

Open your browser:

http://localhost:8501

## Deployment on Render

1. Push your project to GitHub.
2. Log in to [Render](https://render.com).
3. Create a new Web Service.
4. Connect your GitHub repository.
5. Set the following configuration:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run python.py --server.port $PORT --server.address 0.0.0.0
```

6. Add the environment variable in Render:

```text
GROQ_API_KEY = your_groq_api_key
```

7. Click Deploy.

## Security

- Never upload your `.env` file to GitHub.
- Never expose your API keys publicly.
- Use environment variables to store sensitive credentials.

## Author

**Sharmisri N S**

B.Tech Information Technology

GitHub: [sharmi-bit](https://github.com/sharmi-bit)
