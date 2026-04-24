import asyncio
from pathlib import Path

import streamlit as st
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(Path(__file__).with_name(".env"), override=True)

mcp_client = MultiServerMCPClient({

    "mcp-server": {
        "transport": "streamable_http",
        "url": "http://localhost:24000/mcp"

    }
})


async def run_agent(user_query: str) -> str:
    tools = await mcp_client.get_tools()
    llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Answer the user's question using the provided tools. "
            "If the user asks to search, look up, find, or verify live web "
            "information, call the web_search tool before answering. "
            "If the tools cannot answer, say you don't know."
        ),

    )
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": user_query}]
    })
    return response["messages"][-1].content


st.title("Chatbot avec tools")

user_query = st.chat_input("Ask something")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = asyncio.run(run_agent(user_query))
        st.write(answer)


if __name__ == "__main__":
    pass




