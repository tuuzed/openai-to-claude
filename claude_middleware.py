import logging
from typing import Optional, Union

from litellm.caching.dual_cache import DualCache
from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import UserAPIKeyAuth
from litellm.types.utils import CallTypesLiteral

logger = logging.getLogger(__name__)


class ClaudeMiddleware(CustomLogger):
    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: CallTypesLiteral,
    ) -> Optional[Union[Exception, str, dict]]:
        data["model"] = self._mapping_claude_model(data["model"])
        return data

    def _mapping_claude_model(self, model_name: str) -> str:
        if "haiku" in model_name:
            return "claude-haiku"
        elif "sonnet" in model_name:
            return "claude-sonnet"
        elif "opus" in model_name:
            return "claude-opus"
        else:
            return "claude-sonnet"


claude_middleware_instance = ClaudeMiddleware()
