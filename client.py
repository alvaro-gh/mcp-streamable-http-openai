import asyncio
import os
from contextlib import AsyncExitStack

from openai import AsyncOpenAI
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings

class MCPClient:
  def __init__(self):
    self.ai_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

  async def process_query(self, query: str) -> str:
    async with MCPServerStreamableHttp(name='weather', params={'url': 'http://localhost:8000/mcp'}) as server:
      agent = Agent(
        name='Assistant',
        instructions="""
          Utiliza las herramientas para proveer respuestas acerca del estado del tiempo en una ciudad de Argentina.
          Si la herramienta no devuelve información entonces disculpate con un mensaje corto.
          Si la herramienta devuelve alguna característica relacionada al cielo entonces debes responder cómo se encuentra el cielo.
          Si la herramienta devuelve que ademas hay algún tipo de precipitación debes separar la respuesta entre el estado del cielo y las precipitaciones.
          """,
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice='required')
      )

      response = await Runner.run(starting_agent=agent, input=query)
      return response.final_output

  async def chat_loop(self):
    print("\n---Cliente MCP---")
    print("Pregunta por el clima en una ciudad. Escribi exit para salir.")

    while True:
      try:
        query = input("\nQuery: ").strip()

        if query.lower() == "exit":
          break

        response = await self.process_query(query)
        print("\n" + response)

      except Exception as e:
        print(f"\nError: {str(e)}")

async def main():
  client = MCPClient()
  await client.chat_loop()

if __name__ == "__main__":
  asyncio.run(main())