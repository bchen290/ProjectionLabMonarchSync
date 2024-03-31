import asyncio

from dotenv import load_dotenv

from monarchmoneybridge import MonarchMoneyBridge
from projectionlab import ProjectionLab


async def main():
    load_dotenv()
    mm = MonarchMoneyBridge()
    await mm.login()

    pl = ProjectionLab()
    print(pl.exportData({}))
    

if __name__ == "__main__":
    asyncio.run(main())
