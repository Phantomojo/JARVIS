#!/usr/bin/env python3
"""
JARVIS CLI Interface
Unified command-line interface for interacting with the JARVIS autonomous AI system
"""

import asyncio
from jarvis.scripts.autonomous_agent import JarvisAgent
from jarvis.scripts.performance_dashboard import PerformanceDashboard

async def main():
    print("🤖 JARVIS Autonomous AI CLI")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 50)

    agent = JarvisAgent()
    dashboard = PerformanceDashboard()
    dashboard.start()

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("JARVIS: Shutting down. Goodbye!")
                break
            if not user_input:
                continue

            print("\\n🧠 JARVIS processing your request...")
            result = await agent.process_request(user_input)
            print(f"\\n🤖 JARVIS: {result}\\n")

    except KeyboardInterrupt:
        print("\\nJARVIS: Interrupted. Exiting...")

    finally:
        dashboard.stop()

if __name__ == "__main__":
    asyncio.run(main())
