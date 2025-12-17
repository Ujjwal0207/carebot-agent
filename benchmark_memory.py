import asyncio
from app.main import run_agent
from app.memory import clear_memory

async def run_benchmark():
    print("With memory enabled:")
    response_with_memory = await run_agent("Remember that I like Italian food")
    print(response_with_memory)

    print("\nWithout memory:")
    clear_memory()
    response_without_memory = await run_agent("Remember that I like Italian food")
    print(response_without_memory)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
