"""
Configuration module for Pricing Assistant
"""


class Config:
    def __init__(self):
        self.scraping_delay = 2
        self.max_pages = 2
        self.timeout = 30

    def get_vinted_config(self):
        return {
            "base_url": "https://www.vinted.pt",
            "max_retries": 3,
            "delay_between_requests": 1,
        }
