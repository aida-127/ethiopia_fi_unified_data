"""
Data loader for Ethiopia Financial Inclusion Forecasting Challenge
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime
from typing import Dict, Tuple, Optional

class EthiopiaFIDataLoader:
    """Load and validate Ethiopia financial inclusion data"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        self.unified_data = None
        self.reference_codes = None
        self.additional_guide = None
        
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all raw data files"""
        data_dict = {}
        
        # Load unified data
        unified_path = os.path.join(self.data_dir, "ethiopia_fi_unified_data.csv")
        if os.path.exists(unified_path):
            self.unified_data = pd.read_csv(unified_path)
            data_dict['unified_data'] = self.unified_data
            print(f"✓ Loaded unified data: {len(self.unified_data)} records")
        else:
            print(f"✗ File not found: {unified_path}")
            
        # Load reference codes
        ref_path = os.path.join(self.data_dir, "reference_codes.csv")
        if os.path.exists(ref_path):
            self.reference_codes = pd.read_csv(ref_path)
            data_dict['reference_codes'] = self.reference_codes
            print(f"✓ Loaded reference codes: {len(self.reference_codes)} codes")
        else:
            print(f"✗ File not found: {ref_path}")
            
        # Load additional guide (Excel)
        guide_path = os.path.join(self.data_dir, "Additional Data Points Guide.xlsx")
        if os.path.exists(guide_path):
            try:
                # Read all sheets
                self.additional_guide = pd.read_excel(
                    guide_path, 
                    sheet_name=None,
                    header=0
                )
                data_dict['additional_guide'] = self.additional_guide
                print(f"✓ Loaded additional guide with {len(self.additional_guide)} sheets")
            except Exception as e:
                print(f"✗ Error loading Excel file: {e}")
        else:
            print(f"✗ File not found: {guide_path}")
            
        return data_dict
    
    def validate_data(self) -> Dict:
        """Validate data against reference codes"""
        validation_results = {}
        
        if self.unified_data is None or self.reference_codes is None:
            return {"error": "Data not loaded"}
        
        # Check required columns
        required_cols = [
            'record_id', 'record_type', 'category', 'pillar', 
            'indicator', 'indicator_code', 'observation_date'
        ]
        missing_cols = [col for col in required_cols if col not in self.unified_data.columns]
        if missing_cols:
            validation_results['missing_columns'] = missing_cols
        
        # Validate record_type values
        valid_record_types = self.reference_codes[
            self.reference_codes['field'] == 'record_type'
        ]['code'].tolist()
        invalid_record_types = self.unified_data[
            ~self.unified_data['record_type'].isin(valid_record_types)
        ]
        if len(invalid_record_types) > 0:
            validation_results['invalid_record_types'] = invalid_record_types['record_type'].unique()
        
        validation_results['summary'] = {
            'total_records': len(self.unified_data),
            'valid_record_types': valid_record_types,
            'data_quality': 'PASS' if len(validation_results) == 1 else 'NEEDS REVIEW'
        }
        
        return validation_results
    
    def get_data_summary(self) -> Dict:
        """Generate summary statistics of the dataset"""
        if self.unified_data is None:
            return {}
        
        summary = {}
        
        # By record type
        record_type_summary = self.unified_data['record_type'].value_counts().reset_index()
        record_type_summary.columns = ['record_type', 'count']
        record_type_summary['percentage'] = (record_type_summary['count'] / len(self.unified_data) * 100).round(1)
        summary['record_types'] = record_type_summary
        
        # By pillar
        pillar_summary = self.unified_data['pillar'].value_counts().reset_index()
        pillar_summary.columns = ['pillar', 'count']
        summary['pillars'] = pillar_summary
        
        # By source type
        source_summary = self.unified_data['source_type'].value_counts().reset_index()
        source_summary.columns = ['source_type', 'count']
        summary['sources'] = source_summary
        
        # By confidence
        confidence_summary = self.unified_data['confidence'].value_counts().reset_index()
        confidence_summary.columns = ['confidence', 'count']
        summary['confidence'] = confidence_summary
        
        return summary

def generate_record_id(base_id: str, existing_ids: list) -> str:
    """Generate unique record ID"""
    if base_id not in existing_ids:
        return base_id
    
    # Extract prefix and number
    import re
    match = re.match(r'([A-Z]+)_(\d+)', base_id)
    if match:
        prefix, num = match.groups()
        num = int(num)
        while f"{prefix}_{num}" in existing_ids:
            num += 1
        return f"{prefix}_{num:04d}"
    else:
        # Simple increment
        i = 1
        while f"{base_id}_{i}" in existing_ids:
            i += 1
        return f"{base_id}_{i}"