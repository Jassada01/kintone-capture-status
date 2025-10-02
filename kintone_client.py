"""
Kintone API Client Module
Handles authentication and record retrieval from Kintone
"""

import requests
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class KintoneClient:
    def __init__(self):
        self.domain = os.getenv('KINTONE_DOMAIN')
        self.username = os.getenv('KINTONE_USERNAME')
        self.password = os.getenv('KINTONE_PASSWORD')
        self.api_token = os.getenv('KINTONE_API_TOKEN')
        self.app_id = os.getenv('KINTONE_APP_ID')

        if not self.domain or not self.app_id:
            raise ValueError("KINTONE_DOMAIN and KINTONE_APP_ID are required.")

        if not self.api_token and not (self.username and self.password):
            raise ValueError("Either KINTONE_API_TOKEN or (KINTONE_USERNAME and KINTONE_PASSWORD) are required.")

        self.base_url = f"https://{self.domain}"

        # Setup authentication
        if self.api_token:
            self.headers = {'X-Cybozu-API-Token': self.api_token}
            self.auth = None
        else:
            self.headers = {}
            self.auth = (self.username, self.password)

    def get_records(self, query: str = "") -> List[Dict[str, Any]]:
        """
        Fetch records from Kintone app

        Args:
            query: Optional query string to filter records

        Returns:
            List of record dictionaries
        """
        url = f"{self.base_url}/k/v1/records.json"
        params = {
            'app': self.app_id
        }

        if query:
            params['query'] = query

        try:
            response = requests.get(url, headers=self.headers, auth=self.auth, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('records', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching records: {e}")
            return []

    def get_record_url(self, record_id: str) -> str:
        """
        Generate the URL for a specific record

        Args:
            record_id: The record ID

        Returns:
            Full URL to the record detail page
        """
        return f"{self.base_url}/k/{self.app_id}/show#record={record_id}"
