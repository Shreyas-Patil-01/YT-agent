# YT-agent
# YouTube AI Agent 🤖🎥

## Overview
A sophisticated AI-powered YouTube search agent leveraging LangChain, Ollama, and YouTube API to intelligently find and recommend videos.

## Features
- AI-driven YouTube video search
- Local LLM inference with Ollama
- Flexible agent-based search architecture
- Customizable search parameters

## Prerequisites
- Python 3.8+
- YouTube API Key
- Ollama installed locally
- CodeLlama model

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/youtube-ai-agent.git
cd youtube-ai-agent
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
- Create `.env` file
- Add YouTube API key: `YOUTUBE_API_KEY=your_api_key`

## Usage
```bash
python main.py
# Interactively enter search queries
```

## Project Structure
- `main.py`: Entry point
- `ai_agent/`: Agent implementation
  - `youtube_agent.py`: LangChain agent logic
  - `tools.py`: Custom search tools
- `youtube_api/`: YouTube API interactions

## Technologies
- LangChain
- Ollama
- YouTube API
- Python

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and create pull request

## License
MIT License