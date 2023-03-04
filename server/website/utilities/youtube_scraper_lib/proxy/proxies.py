from fp.fp import FreeProxy, FreeProxyException
import os
import requests


class Proxy:
    def __init__(self, region: list[str], rand: bool, website: str):
        self.proxy_server = FreeProxy(region, rand=rand)
        self.website = website
        self.proxy = None
        self.host = None

    def rotate(self):

        self.proxy = None
        self.host = None
        
        while True:
            try:
                proxy = self.proxy_server.get().split("//")
                request_proxy = {proxy[0][:-1]: proxy[1]}
                res = requests.get(self.website, request_proxy, timeout=10)
                if res.status_code == 200:
                    self.proxy = request_proxy
                    self.host = proxy[1]
                    break
            except TimeoutError:
                continue
            except FreeProxyException:
                break

    def get(self) -> dict[str, str]:
        if not self.proxy:
            self.rotate()
            self.set_env()
        return self.proxy

    def set_env(self):
        if self.host:
            request_type = list(self.proxy.keys())[0]
            os.environ[request_type.upper() + "_PROXY"] = self.host
