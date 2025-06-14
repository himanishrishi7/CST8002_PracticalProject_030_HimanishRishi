"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleService class which manages the business logic
for milk sample data. It is part of the Business Layer.
"""

from typing import List, Optional
from src.business.milk_sample_record import MilkSampleRecord
from src.persistence.milk_sample_repository import MilkSampleRepository

class MilkSampleService:
    """
    A service class that manages milk sample data and business logic.
    
    This class is responsible for:
    1. Managing the collection of milk samples
    2. Providing business logic operations on the samples
    3. Coordinating with the persistence layer
    """
    
    def __init__(self):
        """Initialize the service with a repository and empty sample collection."""
        self.repository = MilkSampleRepository()
        self.samples: List[MilkSampleRecord] = []
    
    def load_samples(self, num_samples: int = 6) -> None:
        """
        Load samples from the repository.
        
        Args:
            num_samples (int): Number of samples to load
        """
        self.samples = self.repository.read_samples(num_samples)
    
    def get_sample(self, index: int) -> Optional[MilkSampleRecord]:
        """
        Get a sample by index.
        
        Args:
            index (int): Index of the sample to retrieve
            
        Returns:
            Optional[MilkSampleRecord]: The requested sample or None if not found
        """
        if 0 <= index < len(self.samples):
            return self.samples[index]
        return None
    
    def get_all_samples(self) -> List[MilkSampleRecord]:
        """
        Get all loaded samples.
        
        Returns:
            List[MilkSampleRecord]: List of all samples
        """
        return self.samples
    
    def get_sample_count(self) -> int:
        """
        Get the number of loaded samples.
        
        Returns:
            int: Number of samples
        """
        return len(self.samples) 