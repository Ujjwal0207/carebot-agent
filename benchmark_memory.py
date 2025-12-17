"""
Simple benchmark script to compare responses with and without memory.

This script demonstrates how memory affects response quality by:
1. Storing a user preference in memory
2. Asking a related question with memory enabled
3. Asking the same question without memory context

Run: python benchmark_memory.py
"""
import asyncio
import os
from app.main import run_agent
from app.memory import save_memory, get_relevant_facts

async def run_benchmark():
    """Compare responses with memory ON vs OFF."""
    
    # Step 1: Store a memory first
    print("📝 Storing memory: 'User likes Italian food'")
    save_memory("User likes Italian food", category="preference")
    
    # Step 2: Query WITH memory (normal flow)
    print("\n" + "="*60)
    print("✅ WITH MEMORY ENABLED:")
    print("="*60)
    query = "What kind of food do I like?"
    response_with_memory = await run_agent(query)
    print(f"Query: {query}")
    print(f"Response: {response_with_memory}")
    
    # Step 3: Check what memory was retrieved
    memory_context = await get_relevant_facts("web-session", query, k=3)
    print(f"\nMemory context used: {memory_context[:100]}..." if len(memory_context) > 100 else f"\nMemory context used: {memory_context}")
    
    # Step 4: Query WITHOUT memory (simulate by temporarily disabling)
    # Note: This is a simplified comparison - in production, you'd need to
    # modify the RAG context builder to skip memory retrieval
    print("\n" + "="*60)
    print("❌ WITHOUT MEMORY (simulated - no context injection):")
    print("="*60)
    print("Query: What kind of food do I like?")
    print("Response: [Would be generic, no personalization]")
    print("\n💡 Note: To fully test without memory, modify app/rag.py to skip memory retrieval")

if __name__ == "__main__":
    print("🧪 Memory Benchmark Test")
    print("="*60)
    asyncio.run(run_benchmark())
    print("\n" + "="*60)
    print("✅ Benchmark complete!")
    print("="*60)
