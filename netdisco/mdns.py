"""Add support for discovering mDNS services."""
from typing import List  # noqa: F401

import zeroconf


class MDNS:
    """Base class to discover mDNS services."""

    def __init__(self, zeroconf_instance=None):
        """Initialize the discovery."""
        self.zeroconf = zeroconf_instance
        self._created_zeroconf = False
        self.services = []  # type: List[zeroconf.ServiceInfo]
        self._browser = None  # type: zeroconf.ServiceBrowser

    def register_service(self, service):
        """Register a mDNS service."""
        self.services.append(service)

    def start(self):
        """Start discovery."""
        try:
            if not self.zeroconf:
                self.zeroconf = zeroconf.Zeroconf()
                self._created_zeroconf = True

            def _service_update(*args, **kwargs):
                return

            types = [service.typ for service in self.services]
            self._browser = zeroconf.ServiceBrowser(
                self.zeroconf, types, handlers=[_service_update]
            )
        except Exception:  # pylint: disable=broad-except
            self.stop()
            raise

    def stop(self):
        """Stop discovering."""
        if self._browser:
            self._browser.cancel()
            self._browser = None

        for service in self.services:
            service.reset()

        if self._created_zeroconf:
            self.zeroconf.close()
            self.zeroconf = None

    @property
    def entries(self):
        """Return all entries in the cache."""
        return self.zeroconf.cache.entries()
