import pymongo
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="weather", stateless_http=True, host="127.0.0.1", port=8000)


@mcp.tool()
async def get_weather(city: str) -> str:
    """Get weather information from MongoDB."""
    client = pymongo.MongoClient("localhost", 27017)
    database = client.smn
    collection = database.weather
    r = collection.find_one({"name": city})
    return r["weather"]["description"]  # type: ignore


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
