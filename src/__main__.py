"""Entry point for running the IBM QRadar MCP server"""
import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())

