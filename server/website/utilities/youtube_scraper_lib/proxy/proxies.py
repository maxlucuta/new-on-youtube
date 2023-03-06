import os
import requests
from fp.fp import FreeProxy, FreeProxyException


class Proxy:
    """Class responsible for generating and configuring proxies."""

    def __init__(self, region: list[str], rand: bool, website: str):
        """Constructs a Proxy objext.

        Args:
            region (list[str]): list of region codes, eg. GB, US
            rand (bool): if true allows for random shuffling of proxies
            website (str): intended website for proxy use
        """

        self.proxy_server = FreeProxy(region, rand=rand)
        self.website = website
        self.proxy = None
        self.host = None
        self.used = set()

    def rotate(self):
        """Rotates proxies when called, assumed to be called only if
           previous proxies have been blocked. Wipes previous proxies
           and attemps to generate new ones.
        """

        self.proxy = None
        self.host = None
        while True:
            try:
                proxy_server = self.proxy_server.get()
                if proxy_server in self.used:
                    continue
                request_proxy = {"http" : proxy_server}
                res = requests.get(self.website, request_proxy, timeout=10)
                if res.status_code == 200:
                    self.proxy = request_proxy
                    self.host = proxy_server
                    self.used.add(proxy_server)
                    break
            except TimeoutError:
                continue
            except FreeProxyException:
                break

    def get(self) -> dict[str, str]:
        """Returns most recent proxy generated, if there isn't one
           it will attempt to generate new proxies and update OS
           environmental variables.

        Returns:
            dict[str, str]: http/https proxy in requests format
        """

        self.rotate()
        self.set_env()
        return self.proxy

    def set_env(self):
        """If a proxy has been generated, it will update OS
           environmental variables with the proxy so it can be used
           by external libraries that do not offer request format
           parsing.
        """

        if self.host:
            request_type = list(self.proxy.keys())[0]
            os.environ[request_type.upper() + "_PROXY"] = self.host
