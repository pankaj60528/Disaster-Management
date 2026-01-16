import asyncio
from backend.config import mongo_client

async def test_connection():
    try:
        print("⏳ Connecting to MongoDB...")
        # Ping command to check connection
        await mongo_client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB successfully!")
        
        # Print database name
        print(f"📂 Database Name: {mongo_client.get_default_database().name}")
    except Exception as e:
        print("\n❌ CONNECTION FAILED!")
        print(f"Error Details: {e}")

if __name__ == "__main__":
    # Windows specific fix for asyncio loop
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(test_connection())