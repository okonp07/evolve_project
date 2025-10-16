import pandas as pd
import numpy as np

class DataProcessor:
    """
    Process raw booking data for the recommendation engine.
    Handles feature engineering, aggregation, and statistical computations.
    """
    
    def __init__(self, df):
        """
        Initialize processor with raw dataframe.
        
        Args:
            df: Raw dataframe with columns: property_id, date, booked, price, lead_time, event
        """
        self.df = df.copy()
        self._validate_data()
        
    def _validate_data(self):
        """Validate that required columns exist"""
        required_cols = ['property_id', 'date', 'booked', 'price', 'lead_time', 'event']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Month
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        
        # Week of year
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Is weekend
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Season (Northern Hemisphere)
        df['season'] = df['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        return df
    
    def _calculate_property_stats(self):
        """Calculate property-level aggregated statistics"""
        property_stats = self.df.groupby('property_id').agg({
            'booked': ['mean', 'sum', 'count', 'std'],
            'price': ['mean', 'median', 'std'],
            'lead_time': ['mean', 'median'],
            'event': 'sum'
        }).round(4)
        
        # Flatten column names
        property_stats.columns = ['_'.join(col).strip() for col in property_stats.columns]
        
        # Fill NaN standard deviations with 0
        property_stats['booked_std'] = property_stats['booked_std'].fillna(0)
        property_stats['price_std'] = property_stats['price_std'].fillna(0)
        
        return property_stats
    
    def _calculate_temporal_stats(self):
        """Calculate temporal pattern statistics"""
        temporal_stats = {}
        
        # Day of week statistics
        dow_stats = self.df.groupby('day_name')['booked'].mean()
        for day, rate in dow_stats.items():
            temporal_stats[('day_of_week', day)] = rate
        
        # Month statistics
        month_stats = self.df.groupby('month_name')['booked'].mean()
        for month, rate in month_stats.items():
            temporal_stats[('month', month)] = rate
        
        # Season statistics
        season_stats = self.df.groupby('season')['booked'].mean()
        for season, rate in season_stats.items():
            temporal_stats[('season', season)] = rate
        
        # Weekend vs weekday
        weekend_stats = self.df.groupby('is_weekend')['booked'].mean()
        temporal_stats[('weekend', False)] = weekend_stats.get(0, 0)
        temporal_stats[('weekend', True)] = weekend_stats.get(1, 0)
        
        return temporal_stats
    
    def _calculate_event_stats(self):
        """Calculate event impact statistics"""
        event_stats = self.df.groupby('event').agg({
            'booked': ['mean', 'count'],
            'price': 'mean',
            'lead_time': 'mean'
        }).round(4)
        
        # Flatten column names
        event_stats.columns = ['_'.join(col).strip() for col in event_stats.columns]
        
        return event_stats
    
    def get_summary_statistics(self):
        """Get overall summary statistics of the dataset"""
        summary = {
            'total_records': len(self.df),
            'unique_properties': self.df['property_id'].nunique(),
            'date_range': (self.df['date'].min(), self.df['date'].max()),
            'overall_booking_rate': self.df['booked'].mean(),
            'average_price': self.df['price'].mean(),
            'average_lead_time': self.df['lead_time'].mean(),
            'event_days_pct': (self.df['event'].sum() / len(self.df)) * 100
        }
        return summary Ensure date is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
            self.df['date'] = pd.to_datetime(self.df['date'])
    
    def process(self):
        """
        Process the data and return dictionary of processed dataframes.
        
        Returns:
            Dictionary containing:
                - main_df: Enhanced main dataframe
                - property_stats: Property-level statistics
                - temporal_stats: Temporal pattern statistics
                - event_stats: Event impact statistics
        """
        # Add temporal features
        self.df = self._add_temporal_features(self.df)
        
        # Calculate property-level statistics
        property_stats = self._calculate_property_stats()
        
        # Calculate temporal statistics
        temporal_stats = self._calculate_temporal_stats()
        
        # Calculate event statistics
        event_stats = self._calculate_event_stats()
        
        return {
            'main_df': self.df,
            'property_stats': property_stats,
            'temporal_stats': temporal_stats,
            'event_stats': event_stats
        }
    
    def _add_temporal_features(self, df):
        """Add temporal features to the dataframe"""
        df = df.copy()
        
        # Day of week
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_name'] = df['date'].dt.day_name()
        
        #
