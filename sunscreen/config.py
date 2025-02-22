import configparser
import re


class Config:
    def __init__(self, filename: str):
        self.cp = configparser.ConfigParser()
        self.cp.read(filename)

    def getEnvoyHost(self) -> str:
        return self.cp["Envoy"]["Host"].strip()

    def getEnvoyAccessToken(self) -> str:
        raw = self.cp["Envoy"]["AccessToken"]
        return re.sub(r"\s+", "", raw)

    def getDbPath(self) -> str:
        return self.cp["DB"]["Path"].strip()
