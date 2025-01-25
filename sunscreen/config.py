import configparser
import re


class Config:
    def __init__(self, filename):
        self.cp = configparser.ConfigParser()
        self.cp.read(filename)

    def getEnvoyHost(self):
        return self.cp["Envoy"]["Host"].strip()

    def getEnvoyAccessToken(self):
        raw = self.cp["Envoy"]["AccessToken"]
        return re.sub(r"\s+", "", raw)
