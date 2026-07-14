"""Provider registry for discovering and resolving benchmark data providers."""

from __future__ import annotations

from awcde.providers.base import Provider, ProviderInfo, ProviderSource


class ProviderRegistry:
    """Registry managing available benchmark data providers.

    Providers register themselves by provider_id. The registry can resolve
    which provider to use for a given source based on format detection.
    """

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        """Register a provider instance.

        Args:
            provider: A provider implementing the Provider protocol.
        """
        self._providers[provider.provider_id] = provider

    def get(self, provider_id: str) -> Provider:
        """Retrieve a provider by its ID.

        Args:
            provider_id: The unique identifier of the provider.

        Returns:
            The registered provider instance.

        Raises:
            KeyError: If no provider is registered with the given ID.
        """
        if provider_id not in self._providers:
            raise KeyError(f"No provider registered with id '{provider_id}'")
        return self._providers[provider_id]

    def list_providers(self) -> list[ProviderInfo]:
        """List metadata for all registered providers.

        Returns:
            A list of ProviderInfo objects describing each registered provider.
        """
        result: list[ProviderInfo] = []
        for provider in self._providers.values():
            info = ProviderInfo(
                provider_id=provider.provider_id,
                supported_formats=_get_supported_formats(provider),
                description=_get_description(provider),
            )
            result.append(info)
        return result

    def resolve(self, source: ProviderSource) -> Provider:
        """Find a provider that supports the given source.

        Iterates through registered providers and returns the first one
        whose supports() method returns True.

        Args:
            source: The data source to find a provider for.

        Returns:
            A provider that can handle the source.

        Raises:
            ValueError: If no registered provider supports the source.
        """
        for provider in self._providers.values():
            if provider.supports(source):
                return provider
        registered = list(self._providers.keys())
        raise ValueError(
            f"No provider supports source '{source.filename}' "
            f"(content_type='{source.content_type}'). "
            f"Registered providers: {registered}"
        )


def _get_supported_formats(provider: Provider) -> list[str]:
    """Extract supported formats from a provider, with fallback."""
    if hasattr(provider, "supported_formats"):
        return provider.supported_formats  # type: ignore[attr-defined]
    return []


def _get_description(provider: Provider) -> str:
    """Extract description from a provider, with fallback."""
    if hasattr(provider, "description"):
        return provider.description  # type: ignore[attr-defined]
    return provider.__class__.__doc__ or ""
