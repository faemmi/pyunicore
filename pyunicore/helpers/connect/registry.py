import logging
from typing import Dict

import pyunicore.client

from pyunicore.helpers.connect import site as _site
from pyunicore import credentials

logger = logging.getLogger(__name__)


def connect_to_registry(
    registry_url: str, credentials: credentials.Credential
) -> pyunicore.client.Registry:
    """Connect to a registry.

    Args:
        registry_url (str): URL to the UNICORE registry.
        credentials (pyunicore.credentials.Credential): Authentication method.

    Returns:
        pyunicore.client.Registry

    """
    logger.info("Attempting to connect to registry %s", registry_url)
    transport = pyunicore.client.Transport(credentials)
    return pyunicore.client.Registry(transport=transport, url=registry_url)


def connect_to_site_from_registry(
    registry_url: str, site_name: str, credentials: credentials.Credential
) -> pyunicore.client.Client:
    """Create a connection to a site's UNICORE API from the registry base URL.

    Args:
        registry_url (str): URL to the UNICORE registry.
        site_name (str): Name of the site to connect to.
        credentials (pyunicore.credentials.Credential): Authentication method.

    Raises:
        ValueError: Site not available in the registry.

    Returns:
        pyunicore.client.Client

    """
    logger.info(
        "Attempting to connect to %s from registry %s", site_name, registry_url
    )
    transport = pyunicore.client.Transport(credentials)
    site_api_url = _get_site_api_url(
        site=site_name,
        registry_url=registry_url,
        transport=transport,
    )
    client = _site.connect_to_site(
        site_api_url=site_api_url,
        credentials=credentials,
    )
    return client


def _get_site_api_url(
    site: str,
    transport: pyunicore.client.Transport,
    registry_url: str,
) -> str:
    logger.debug(
        "Attempting to get site REST API URL for %s from registry %s",
        site,
        registry_url,
    )
    api_urls = _get_api_urls(transport=transport, registry_url=registry_url)
    logger.debug("Available API URLs: %s", api_urls)
    try:
        api_url = api_urls[site]
    except KeyError:
        available_sites_list = list(api_urls.keys())
        available_sites = ", ".join(available_sites_list)
        raise ValueError(
            f"Site {site} not available in registry {registry_url}. "
            f"Available sites: {available_sites}."
        )
    return api_url


def _get_api_urls(
    transport: pyunicore.client.Transport, registry_url: str
) -> Dict[str, str]:
    logger.debug(
        "Getting all available API URLs from registry %s", registry_url
    )
    registry = pyunicore.client.Registry(transport=transport, url=registry_url)
    return registry.site_urls
