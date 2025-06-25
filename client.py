import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings


class MCPClient:
    """Client MCP Class."""

    async def process_query(self, query: str) -> str:
        """Process incoming queries to this client."""
        async with MCPServerStreamableHttp(
            name="weather", params={"url": "http://localhost:8000/mcp"}
        ) as server:
            agent = Agent(
                name="Assistant",
                instructions="""
          Use tools to provide answers about the weather in Argentina cities.
          If the tool does not return information then make a short apology.
          The tool returns one or few words so adapt your answer to a short sentence.
          The tool returns words in spanish so translate your final answer to english.
          """,
                mcp_servers=[server],
                model_settings=ModelSettings(tool_choice="required"),
            )

            response = await Runner.run(starting_agent=agent, input=query)
            return response.final_output

    async def chat_loop(self) -> None:
        """Chat with user on a loop."""
        print("---MCP Client---")  # noqa: T201
        print(  # noqa: T201
            "Ask about the weather in a city (Argentina). Type exit to finish the chat."
        )

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "exit":
                    break
                response = await self.process_query(query)
                print("\n" + response)  # noqa: T201
            except Exception as e:
                print(f"\nError: {e}")  # noqa: T201


async def main() -> None:
    """Run the client."""
    client = MCPClient()
    await client.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
