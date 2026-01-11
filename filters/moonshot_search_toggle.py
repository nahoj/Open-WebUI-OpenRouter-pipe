"""
title: Moonshot Search
author: Open-WebUI-OpenRouter-pipe
author_url: https://github.com/rbb-dev/Open-WebUI-OpenRouter-pipe
id: moonshot_search
description: Enables Moonshot/Kimi builtin $web_search tool and disables Open WebUI Web Search for this request.
version: 0.1.0
license: MIT
"""

from __future__ import annotations

import logging
from typing import Any

try:
    from open_webui.env import SRC_LOG_LEVELS
except ImportError:
    SRC_LOG_LEVELS = {}


_BUILTIN_WEB_SEARCH = {
    "type": "builtin_function",
    "function": {"name": "$web_search"},
}


class Filter:
    # Toggleable filter (shows a switch in the Integrations menu).
    toggle = True

    def __init__(self) -> None:
        self.log = logging.getLogger("moonshot.web_search.toggle")
        self.log.setLevel(SRC_LOG_LEVELS.get("OPENAI", logging.INFO))
        self.toggle = True

    def inlet(
        self,
        body: dict[str, Any],
        __metadata__: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if __metadata__ is not None and not isinstance(__metadata__, dict):
            return body

        features = body.get("features")
        if not isinstance(features, dict):
            features = {}
            body["features"] = features

        # Enforce: builtin web search overrides Open WebUI native web search handler.
        features["web_search"] = False

        tools = body.get("tools")
        if not isinstance(tools, list):
            tools = []
            body["tools"] = tools

        if not any(
            isinstance(tool, dict)
            and tool.get("type") == "builtin_function"
            and isinstance(tool.get("function"), dict)
            and tool.get("function", {}).get("name") == "$web_search"
            for tool in tools
        ):
            tools.append(dict(_BUILTIN_WEB_SEARCH))

        if isinstance(__metadata__, dict):
            meta_features = __metadata__.get("features")
            if meta_features is None:
                meta_features = {}
                __metadata__["features"] = meta_features

            if meta_features is features:
                meta_features = dict(meta_features)
                __metadata__["features"] = meta_features

            if isinstance(meta_features, dict):
                meta_features["web_search"] = False

        self.log.debug("Enabled Moonshot $web_search; disabled Open WebUI web_search")
        return body
