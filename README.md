# MCP streamable http with OpenAI PoC

I'm learning about MCP with the new streamable HTTP transport. This is just a very small, quick and dirty example of MCP client-server communication using streamable-http as the transport. I'm actually learning about all of this and there are tons of concepts which require spending more time reading. Anyway, there aren't many simple examples out there, this one is for myself and for whoever might find it useful.

## Requirements

This requires using OpenAI models so you need the `OPENAI_API_KEY` environment variable set.

## Instructions

```
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

### Run the stack

**Run the SMN data fetch**

```
$ docker run -p 27017:27017 mongo:latest
$ uv run smn2mongo.py
```

**Run the MCP Server**

```
$ uv run server.py
# Can also use inspector
$ mcp dev server.py
```

**Run the MCP Client**

```
$ uv run client.py
```

## Sample interaction

This is in spanish right now, the idea is that you can ask about the current weather on _supported_ cities, meaning the cities included in the data obtained from the argentinian weather service. Sample of weather data:

```json
{
  "name": "Chapelco",
  "province": "Neuquén",
  "weather": {
    "description": "Nublado con llovizna"
  }
},
{
  "name": "General Alvear",
  "province": "Mendoza",
  "weather": {
    "description": "Cubierto con neblina"
  }
}
```

```
$ uv run client.py

---Cliente MCP---
Pregunta por el clima en una ciudad. Escribi exit para salir.

Query: how's the weather in Mendoza?

Weather in Mendoza is cloudy

```


## Resources

* https://github.com/invariantlabs-ai/mcp-streamable-http/tree/main
* https://github.com/openai/openai-agents-python/tree/main/examples/mcp/streamablehttp_example
* https://www.philschmid.de/mcp-example-llama
