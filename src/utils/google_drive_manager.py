"""
Google Drive Manager for IronDome Mosquitoes Project

This module handles uploading detection images and videos to Google Drive
for backup and sharing purposes.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from .logger import get_logger

logger = get_logger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveManager:
    """Manages Google Drive operations for the IronDome Mosquitoes project."""
    
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        """
        Initialize the Google Drive Manager.
        
        Args:
            credentials_path: Path to the Google API credentials file
            token_path: Path to store the authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.folder_id = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Google Drive API.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    return False
            else:
                if not os.path.exists(self.credentials_path):
                    logger.error(f"Credentials file not found: {self.credentials_path}")
                    logger.info("Please download credentials.json from Google Cloud Console")
                    return False
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
                
        try:
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Successfully authenticated with Google Drive")
            return True
        except Exception as e:
            logger.error(f"Failed to build Drive service: {e}")
            return False
            
    def create_project_folder(self, folder_name: str = "IronDome Mosquitoes") -> Optional[str]:
        """
        Create a folder in Google Drive for the project.
        
        Args:
            folder_name: Name of the folder to create
            
        Returns:
            str: Folder ID if successful, None otherwise
        """
        if not self.service:
            logger.error("Not authenticated with Google Drive")
            return None
            
        try:
            # Check if folder already exists
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                self.folder_id = files[0]['id']
                logger.info(f"Using existing folder: {folder_name} (ID: {self.folder_id})")
                return self.folder_id
                
            # Create new folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            self.folder_id = folder.get('id')
            logger.info(f"Created new folder: {folder_name} (ID: {self.folder_id})")
            return self.folder_id
            
        except HttpError as error:
            logger.error(f"Failed to create folder: {error}")
            return None
            
    def create_date_folder(self, date: datetime) -> Optional[str]:
        """
        Create a date-specific folder within the project folder.
        
        Args:
            date: Date for the folder name
            
        Returns:
            str: Folder ID if successful, None otherwise
        """
        if not self.folder_id:
            logger.error("Project folder not created")
            return None
            
        folder_name = date.strftime("%Y-%m-%d")
        
        try:
            # Check if folder already exists
            query = f"name='{folder_name}' and '{self.folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                logger.info(f"Using existing date folder: {folder_name}")
                return files[0]['id']
                
            # Create new date folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.folder_id]
            }
            
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            folder_id = folder.get('id')
            logger.info(f"Created new date folder: {folder_name} (ID: {folder_id})")
            return folder_id
            
        except HttpError as error:
            logger.error(f"Failed to create date folder: {error}")
            return None
            
    def upload_file(self, file_path: str, folder_id: Optional[str] = None, 
                   description: str = "") -> Optional[str]:
        """
        Upload a file to Google Drive.
        
        Args:
            file_path: Path to the file to upload
            folder_id: ID of the folder to upload to (uses project folder if None)
            description: Description for the file
            
        Returns:
            str: File ID if successful, None otherwise
        """
        if not self.service:
            logger.error("Not authenticated with Google Drive")
            return None
            
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
            
        try:
            file_metadata = {
                'name': os.path.basename(file_path),
                'description': description
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            elif self.folder_id:
                file_metadata['parents'] = [self.folder_id]
                
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            logger.info(f"Uploaded file: {os.path.basename(file_path)} (ID: {file_id})")
            return file_id
            
        except HttpError as error:
            logger.error(f"Failed to upload file {file_path}: {error}")
            return None
            
    def upload_detection_files(self, detection_dir: str, date: datetime) -> Dict[str, Any]:
        """
        Upload all detection files for a specific date.
        
        Args:
            detection_dir: Directory containing detection files
            date: Date of the detections
            
        Returns:
            Dict containing upload results
        """
        results = {
            'success': [],
            'failed': [],
            'total_files': 0,
            'uploaded_files': 0
        }
        
        if not self.service:
            logger.error("Not authenticated with Google Drive")
            results['failed'].append("Not authenticated")
            return results
            
        # Create date folder
        date_folder_id = self.create_date_folder(date)
        if not date_folder_id:
            results['failed'].append("Failed to create date folder")
            return results
            
        # Find all files in detection directory
        detection_path = Path(detection_dir)
        if not detection_path.exists():
            results['failed'].append(f"Detection directory not found: {detection_dir}")
            return results
            
        # Get all image and video files
        file_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov']
        files = []
        for ext in file_extensions:
            files.extend(detection_path.glob(f"*{ext}"))
            files.extend(detection_path.glob(f"*{ext.upper()}"))
            
        results['total_files'] = len(files)
        
        for file_path in files:
            try:
                description = f"Mosquito detection from {date.strftime('%Y-%m-%d %H:%M:%S')}"
                file_id = self.upload_file(str(file_path), date_folder_id, description)
                
                if file_id:
                    results['success'].append({
                        'file': file_path.name,
                        'id': file_id
                    })
                    results['uploaded_files'] += 1
                else:
                    results['failed'].append(str(file_path))
                    
            except Exception as e:
                logger.error(f"Error uploading {file_path}: {e}")
                results['failed'].append(str(file_path))
                
        logger.info(f"Upload complete: {results['uploaded_files']}/{results['total_files']} files uploaded")
        return results
        
    def list_files(self, folder_id: Optional[str] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        List files in a Google Drive folder.
        
        Args:
            folder_id: ID of the folder to list (uses project folder if None)
            max_results: Maximum number of results to return
            
        Returns:
            List of file information dictionaries
        """
        if not self.service:
            logger.error("Not authenticated with Google Drive")
            return []
            
        try:
            query = f"'{folder_id or self.folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id, name, mimeType, createdTime, size)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Found {len(files)} files in folder")
            return files
            
        except HttpError as error:
            logger.error(f"Failed to list files: {error}")
            return []
            
    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from Google Drive.
        
        Args:
            file_id: ID of the file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            logger.error("Not authenticated with Google Drive")
            return False
            
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"Deleted file: {file_id}")
            return True
            
        except HttpError as error:
            logger.error(f"Failed to delete file {file_id}: {error}")
            return False 