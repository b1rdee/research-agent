"# research-agent" 

# 🔍 Ask Birdy – AI Research Agent

**Ask Birdy** is a Streamlit-based web application that researches any topic you ask. It uses two AI agents (Researcher and Writer) powered by **CrewAI** and **Google Gemini** to find up-to-date information via web search (Serper API) and produce a detailed, well‑structured summary.

👉 **Live demo (GitHub‑built version):** https://research-agent-df-production-0e06.up.railway.app/

👉 **Live demo (pre-built image push version):** https://research-agent-production-42cb.up.railway.app/


---

## ✨ Features

- Natural language input – just type a topic  
- Multi‑agent research (web search + summarisation)  
- Real‑time progress streaming (optional)  
- Dockerised – runs anywhere  
- Two deployment options: **Git‑based CD** or **pre‑built image push**

---

## 🛠️ Tech Stack

| Layer       | Technology                                                                 |
|-------------|----------------------------------------------------------------------------|
| Frontend    | [Streamlit](https://streamlit.io)                                          |
| LLM & Agents| [CrewAI](https://docs.crewai.com) + [Google Gemini API](https://ai.google.dev/gemini-api) |
| Web Search  | [Serper API](https://serper.dev)                                           |
| Container   | Docker                                                                     |
| Deployment  | [Railway](https://railway.app)                                             |

---

## 🚀 Getting Started (Local Development)

**Prerequisites**

- Python 3.9+
- Docker (optional, but recommended)
- API keys: [Gemini](https://aistudio.google.com/app/apikey) + [Serper](https://serper.dev)

1. **Clone the repository**

   ```bash
   git clone https://github.com/b17dyE/research-agent.git
   cd research-agent
2.  **Set up environment variables**

Create a .env file:

GEMINI_API_KEY=your_gemini_key_here

SERPER_API_KEY=your_serper_key_here

⚠️ Never commit .env – it's already ignored via .gitignore.

3.  **Run without Docker**

```bash
pip install -r requirements.txt
streamlit run app.py
Open http://localhost:8501
```

4. **Run with Docker (test the container)**

```bash
docker build -t research-agent .
docker run -p 7860:7860 research-agent
Then visit http://localhost:7860.
```

---

# Deployment on Railway – Two Methods
Railway offers two industry‑standard ways to deploy a Dockerised app.

**Method 1: Git‑Based Deployment (CI/CD) – Recommended for active development**

- Your code lives on GitHub; Railway builds from the Dockerfile on every push.

- Push your code to a GitHub repository.

- On Railway.app, create a new project → Deploy from GitHub repo.

- Select your repository and branch. Railway automatically detects the Dockerfile.

- Add environment variables (GEMINI_API_KEY, SERPER_API_KEY) in the Variables tab.

- Railway assigns a public URL. Every git push triggers an automatic redeploy.

- Pros: Always in sync with your source code, full version control, no manual image builds.

**Method 2: Pre‑built Image Deployment (Push a Docker image)**

- Build the image once on your local machine and push it to a registry (Docker Hub or GitHub Container Registry), then deploy on Railway.

- Build your Docker image locally:

```bash
docker build -t research-agent .
```
- Tag it for your registry (using Docker Hub as an example):


```bash
docker tag research-agent YOUR_DOCKER_USERNAME/research-agent:latest
```
- Push to Docker Hub:


```bash
docker push YOUR_DOCKER_USERNAME/research-agent:latest
```

- On Railway, create a new project → Deploy from Docker Image.

- Enter the image name (e.g., YOUR_DOCKER_USERNAME/research-agent:latest).

- Add the same environment variables in the Variables tab.

- Railway pulls the image and runs it.

- Pros: You keep full control over the exact image contents; no need to expose your Dockerfile or source code (if you prefer private source).

Both methods produce a live, publicly accessible agent. The Git‑based method is simpler for ongoing development; the image‑based method is useful for distributing a pre‑built artifact.

---

# How It Works (Agent Flow)

- User enters a topic in the Streamlit interface.

- Researcher agent uses SerperDevTool to search the web for up‑to‑date information (respecting current date, ignoring future dates).

- Writer agent transforms the research into a detailed, easy‑to‑read summary (500+ words).

- The final answer is displayed.

- Orchestration is handled by CrewAI (sequential process).

--- 

# Project Structure

```text
research-agent/
├── app.py               # Streamlit frontend
├── crew.py              # CrewAI agents, tasks, and Gemini LLM setup
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container definition
├── .env                 # API keys (not committed)
├── .gitignore           # Ignores .env, __pycache__, etc.
└── README.md            # This file
```



    
