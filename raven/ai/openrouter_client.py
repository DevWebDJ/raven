import frappe
import requests
from typing import Optional
import frappe

class OpenRouterClient:
    def __init__(self):
        raven_settings = frappe.get_cached_doc("Raven Settings")
        self.api_key = raven_settings.get_password("openrouter_api_key")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": raven_settings.openrouter_http_referer or "https://raven.com",
            "X-Title": raven_settings.openrouter_app_name or "Raven Chat", 
            "Content-Type": "application/json"
        }

    def create_chat_completion(self, model: str, messages: list, **kwargs):
        url = f"{self.base_url}/chat/completions"
        headers = {**self.default_headers, "Content-Type": "application/json"}
        
        payload = {
            "model": model,
            "messages": messages,
            **kwargs
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"OpenRouter API Error: {str(e)}")
            raise

def get_openrouter_client() -> Optional[OpenRouterClient]:
    if frappe.conf.get("openrouter_api_key"):
        return OpenRouterClient()
    return None
