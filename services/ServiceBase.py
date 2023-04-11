from typing import Any, Dict

# Define a base class for plugins
class ServiceBase:
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        pass