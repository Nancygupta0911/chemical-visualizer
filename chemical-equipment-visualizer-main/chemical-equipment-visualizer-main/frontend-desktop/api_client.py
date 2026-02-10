import requests
import json

class APIClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def upload_csv(self, file_path):
        """Upload CSV file to backend"""
        url = f"{self.base_url}/datasets/upload/"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(url, files=files)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Upload failed: {str(e)}")
    
    def get_datasets(self):
        """Get list of all datasets"""
        url = f"{self.base_url}/datasets/"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch datasets: {str(e)}")
    
    def get_dataset(self, dataset_id):
        """Get specific dataset by ID"""
        url = f"{self.base_url}/datasets/{dataset_id}/"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch dataset: {str(e)}")
    
    def download_pdf(self, dataset_id, save_path):
        """Download PDF report"""
        url = f"{self.base_url}/datasets/{dataset_id}/download_pdf/"
        
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download PDF: {str(e)}")
    
    def health_check(self):
        """Check if backend is running"""
        url = f"{self.base_url}/health/"
        
        try:
            response = self.session.get(url, timeout=3)
            response.raise_for_status()
            return True
        except:
            return False