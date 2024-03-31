import asyncio
import os
from monarchmoney import MonarchMoney, RequireMFAException


class MonarchMoneyBridge():
    def __init__(self) -> None:
        self._email = os.getenv("MONARCHMONEY_EMAIL")
        self._password = os.getenv("MONARCHMONEY_PASSWORD")
        self._mfa = os.getenv("MONARCHMONEY_MFA_CODE")

        self.mm = MonarchMoney()
    
    async def login(self):
        if os.path.exists(self.mm._session_file):
            print("Session file found. Attempting to load session...")
            self.mm.load_session()
        else:
            try:
                await self.mm.login(self._email, self._password)
            except RequireMFAException:
                await self.mm.multi_factor_authenticate(self._email, self._password, self._mfa)
