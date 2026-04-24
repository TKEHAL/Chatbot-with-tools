# Mutiagents MCP

A small MCP-based agent project that exposes local tools through an MCP server and consumes them from a Streamlit chat app using LangChain.

The project currently includes:

- An MCP server running on Streamable HTTP
- A Tavily-powered `web_search` tool for live web search
- A sample `get_employee_infos` tool
- A Streamlit chat interface connected to the MCP server
- A Groq chat model client through LangChain

## Project Structure

```text
.
├── agent_graph.py      # Streamlit chat app / LangChain agent client
├── mcp-server.py       # MCP server exposing tools
├── .env.example        # Safe environment variable template
├── pyproject.toml      # Project metadata and dependencies
└── README.md
```

## Requirements

- Python 3.14 or newer
- `uv`
- Tavily API key
- Groq API key

## Setup

Install dependencies:

```bash
uv sync
```

Create your local environment file:

```bash
cp .env.example .env
```

Then fill in `.env`:

```env
TAVILY_API_KEY=your_real_tavily_api_key
GROQ_API_KEY=your_real_groq_api_key
```

Do not commit `.env`. It contains private credentials and should stay local.

## Run The MCP Server

Start the MCP server in one terminal:

```bash
uv run mcp-server.py
```

The server listens on:

```text
http://localhost:24000/mcp
```

Available tools:

- `web_search`: searches the live web using Tavily
- `get_employee_infos`: returns sample employee data

## Run The Agent App

In a second terminal, start the Streamlit app:

```bash
uv run streamlit run agent_graph.py
```

Open the Streamlit URL shown in the terminal, then ask a question. If the question requires current or live information, the agent is instructed to call the `web_search` MCP tool.

## Environment Variables

| Variable | Description |
| --- | --- |
| `TAVILY_API_KEY` | API key used by the Tavily search tool |
| `GROQ_API_KEY` | API key used by the Groq chat model |

## Security Notes

- Keep `.env` out of Git.
- Commit `.env.example` only with placeholder values.
- If a real key was ever committed, rotate it immediately from the provider dashboard.
- If secrets were pushed to GitHub, remove them from Git history before making the repository public.

## Development Notes

The Streamlit app connects to the MCP server with:

```python
MultiServerMCPClient({
    "mcp-server": {
        "transport": "streamable_http",
        "url": "http://localhost:24000/mcp",
    }
})
```

The MCP server loads `.env` from the project directory before initializing tools, so API keys are available when the server starts.
