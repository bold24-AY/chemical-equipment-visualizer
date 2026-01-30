"""
API Client for communicating with Django backend.
"""
import requests
from requests.auth import HTTPBasicAuth


class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, username, password):
        """
        Authenticate user and create session.
        """
        url = f"{self.base_url}/login/"
        response = self.session.post(url, json={
            'username': username,
            'password': password
        })
        response.raise_for_status()
        
        # Extract CSRF token and set header for future requests
        if 'csrftoken' in self.session.cookies:
            self.session.headers.update({'X-CSRFToken': self.session.cookies['csrftoken']})
            
        return response.json()
    
    def logout(self):
        """
        Logout current user.
        """
        url = f"{self.base_url}/logout/"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
    
    def check_auth(self):
        """
        Check if session is authenticated.
        """
        url = f"{self.base_url}/check-auth/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except:
            return {'authenticated': False}
    
    def upload_csv(self, file_path):
        """
        Upload CSV file to backend.
        """
        url = f"{self.base_url}/upload/"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        response.raise_for_status()
        return response.json()
    
    def get_summary(self):
        """
        Get latest dataset summary.
        """
        url = f"{self.base_url}/summary/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_history(self):
        """
        Get last 5 uploads.
        """
        url = f"{self.base_url}/history/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id):
        """
        Get specific dataset by ID.
        """
        url = f"{self.base_url}/dataset/{dataset_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id=None, save_path="report.pdf"):
        """
        Download PDF report.
        """
        url = f"{self.base_url}/report/"
        if dataset_id:
            url = f"{self.base_url}/report/{dataset_id}/"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return save_path
