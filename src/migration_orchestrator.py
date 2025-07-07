"""
Multi-Cloud Migration Orchestrator
Manages data migration and analytics across multiple cloud platforms
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import random

class MultiCloudMigrationOrchestrator:
    """Orchestrate data migration across multiple cloud platforms"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.cloud_providers = {
            'AWS': {
                'services': ['S3', 'Redshift', 'EMR', 'Glue', 'QuickSight'],
                'regions': ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1'],
                'cost_factor': 1.0
            },
            'GCP': {
                'services': ['Cloud Storage', 'BigQuery', 'Dataflow', 'Dataproc', 'Looker'],
                'regions': ['us-central1', 'us-west1', 'europe-west1', 'asia-southeast1'],
                'cost_factor': 0.9
            },
            'Azure': {
                'services': ['Blob Storage', 'Synapse', 'Data Factory', 'HDInsight', 'Power BI'],
                'regions': ['East US', 'West US 2', 'West Europe', 'Southeast Asia'],
                'cost_factor': 1.1
            }
        }
        
        self.data_types = [
            'transactional', 'analytical', 'streaming', 'batch',
            'structured', 'unstructured', 'semi-structured'
        ]
        
        self.migration_strategies = [
            'lift_and_shift', 'replatform', 'refactor', 'hybrid'
        ]
    
    def generate_migration_projects(self, num_projects: int = 20) -> pd.DataFrame:
        """Generate migration project data"""
        projects = []
        
        for i in range(num_projects):
            source_cloud = np.random.choice(list(self.cloud_providers.keys()))
            target_cloud = np.random.choice([c for c in self.cloud_providers.keys() if c != source_cloud])
            
            data_size_gb = np.random.lognormal(8, 2)  # Log-normal distribution for data sizes
            complexity_score = np.random.uniform(1, 10)
            
            # Migration timeline based on complexity and data size
            base_days = max(30, data_size_gb / 100 + complexity_score * 5)
            migration_days = int(np.random.normal(base_days, base_days * 0.2))
            
            start_date = datetime.now() - timedelta(days=np.random.randint(0, 180))
            end_date = start_date + timedelta(days=migration_days)
            
            # Cost calculation
            base_cost = data_size_gb * 10 + complexity_score * 1000
            source_factor = self.cloud_providers[source_cloud]['cost_factor']
            target_factor = self.cloud_providers[target_cloud]['cost_factor']
            
            migration_cost = base_cost * (source_factor + target_factor) / 2
            
            project = {
                'project_id': f'MIG_{i+1:03d}',
                'project_name': f'Migration Project {i+1}',
                'source_cloud': source_cloud,
                'target_cloud': target_cloud,
                'data_type': np.random.choice(self.data_types),
                'data_size_gb': round(data_size_gb, 2),
                'complexity_score': round(complexity_score, 1),
                'migration_strategy': np.random.choice(self.migration_strategies),
                'start_date': start_date,
                'end_date': end_date,
                'estimated_cost_usd': round(migration_cost, 2),
                'status': np.random.choice(['Planning', 'In Progress', 'Completed', 'On Hold'], 
                                         p=[0.2, 0.4, 0.3, 0.1]),
                'team_size': np.random.randint(3, 12),
                'business_unit': np.random.choice(['Finance', 'Marketing', 'Operations', 'IT', 'HR'])
            }
            
            projects.append(project)
        
        return pd.DataFrame(projects)
    
    def generate_performance_metrics(self, projects_df: pd.DataFrame) -> pd.DataFrame:
        """Generate performance metrics for migration projects"""
        metrics = []
        
        for _, project in projects_df.iterrows():
            if project['status'] in ['In Progress', 'Completed']:
                # Generate daily metrics during migration period
                current_date = project['start_date']
                end_date = min(project['end_date'], datetime.now())
                
                while current_date <= end_date:
                    # Performance metrics
                    throughput_gbps = max(0.1, np.random.normal(2.5, 0.8))
                    latency_ms = max(10, np.random.normal(150, 50))
                    error_rate = max(0, np.random.normal(0.02, 0.01))
                    
                    # Cost metrics
                    daily_cost = project['estimated_cost_usd'] / (project['end_date'] - project['start_date']).days
                    actual_daily_cost = daily_cost * np.random.normal(1.0, 0.15)
                    
                    metric = {
                        'project_id': project['project_id'],
                        'date': current_date.date(),
                        'throughput_gbps': round(throughput_gbps, 2),
                        'latency_ms': round(latency_ms, 1),
                        'error_rate': round(error_rate, 4),
                        'daily_cost_usd': round(actual_daily_cost, 2),
                        'data_transferred_gb': round(throughput_gbps * 24 * 3600 / 8, 2),
                        'cpu_utilization': round(np.random.uniform(40, 85), 1),
                        'memory_utilization': round(np.random.uniform(50, 90), 1)
                    }
                    
                    metrics.append(metric)
                    current_date += timedelta(days=1)
        
        return pd.DataFrame(metrics)
    
    def generate_cost_analysis(self, projects_df: pd.DataFrame) -> pd.DataFrame:
        """Generate detailed cost analysis"""
        cost_breakdown = []
        
        for _, project in projects_df.iterrows():
            # Break down costs by category
            total_cost = project['estimated_cost_usd']
            
            breakdown = {
                'project_id': project['project_id'],
                'compute_cost': total_cost * 0.4,
                'storage_cost': total_cost * 0.25,
                'network_cost': total_cost * 0.15,
                'tools_cost': total_cost * 0.1,
                'personnel_cost': total_cost * 0.1,
                'source_cloud': project['source_cloud'],
                'target_cloud': project['target_cloud'],
                'data_size_gb': project['data_size_gb']
            }
            
            # Add variance
            for cost_type in ['compute_cost', 'storage_cost', 'network_cost', 'tools_cost', 'personnel_cost']:
                breakdown[cost_type] *= np.random.normal(1.0, 0.1)
                breakdown[cost_type] = round(breakdown[cost_type], 2)
            
            cost_breakdown.append(breakdown)
        
        return pd.DataFrame(cost_breakdown)
    
    def analyze_migration_patterns(self, projects_df: pd.DataFrame) -> Dict:
        """Analyze migration patterns and trends"""
        analysis = {
            'cloud_preferences': {
                'source_distribution': projects_df['source_cloud'].value_counts().to_dict(),
                'target_distribution': projects_df['target_cloud'].value_counts().to_dict()
            },
            'migration_strategies': projects_df['migration_strategy'].value_counts().to_dict(),
            'data_types': projects_df['data_type'].value_counts().to_dict(),
            'average_metrics': {
                'avg_data_size_gb': projects_df['data_size_gb'].mean(),
                'avg_complexity': projects_df['complexity_score'].mean(),
                'avg_cost_usd': projects_df['estimated_cost_usd'].mean(),
                'avg_team_size': projects_df['team_size'].mean()
            },
            'status_distribution': projects_df['status'].value_counts().to_dict()
        }
        
        return analysis
    
    def generate_recommendations(self, projects_df: pd.DataFrame, 
                               performance_df: pd.DataFrame) -> List[Dict]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Analyze performance issues
        if len(performance_df) > 0:
            high_latency_projects = performance_df[performance_df['latency_ms'] > 200]['project_id'].unique()
            high_error_projects = performance_df[performance_df['error_rate'] > 0.05]['project_id'].unique()
            
            for project_id in high_latency_projects:
                recommendations.append({
                    'project_id': project_id,
                    'type': 'Performance',
                    'issue': 'High Latency',
                    'recommendation': 'Consider optimizing network configuration or using dedicated connections',
                    'priority': 'High',
                    'estimated_savings_usd': np.random.uniform(1000, 5000)
                })
            
            for project_id in high_error_projects:
                recommendations.append({
                    'project_id': project_id,
                    'type': 'Reliability',
                    'issue': 'High Error Rate',
                    'recommendation': 'Implement better error handling and retry mechanisms',
                    'priority': 'Critical',
                    'estimated_savings_usd': np.random.uniform(2000, 8000)
                })
        
        # Cost optimization recommendations
        expensive_projects = projects_df[projects_df['estimated_cost_usd'] > projects_df['estimated_cost_usd'].quantile(0.8)]
        
        for _, project in expensive_projects.iterrows():
            recommendations.append({
                'project_id': project['project_id'],
                'type': 'Cost Optimization',
                'issue': 'High Migration Cost',
                'recommendation': f'Consider {project["migration_strategy"]} strategy optimization',
                'priority': 'Medium',
                'estimated_savings_usd': project['estimated_cost_usd'] * 0.15
            })
        
        return recommendations

if __name__ == "__main__":
    # Generate multi-cloud migration data
    orchestrator = MultiCloudMigrationOrchestrator()
    
    print("Generating migration projects...")
    projects = orchestrator.generate_migration_projects(25)
    
    print("Generating performance metrics...")
    performance = orchestrator.generate_performance_metrics(projects)
    
    print("Generating cost analysis...")
    costs = orchestrator.generate_cost_analysis(projects)
    
    print("Analyzing migration patterns...")
    patterns = orchestrator.analyze_migration_patterns(projects)
    
    print("Generating recommendations...")
    recommendations = orchestrator.generate_recommendations(projects, performance)
    
    # Save data
    import os
    os.makedirs('../data', exist_ok=True)
    
    projects.to_csv('../data/migration_projects.csv', index=False)
    performance.to_csv('../data/performance_metrics.csv', index=False)
    costs.to_csv('../data/cost_analysis.csv', index=False)
    
    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df.to_csv('../data/recommendations.csv', index=False)
    
    # Save analysis results
    with open('../data/migration_analysis.json', 'w') as f:
        json.dump(patterns, f, indent=2, default=str)
    
    print(f"\n=== Dataset Summary ===")
    print(f"Migration Projects: {len(projects)} records")
    print(f"Performance Metrics: {len(performance)} records")
    print(f"Cost Analysis: {len(costs)} records")
    print(f"Recommendations: {len(recommendations)} records")
    print(f"Cloud Providers: {list(orchestrator.cloud_providers.keys())}")
    print(f"Migration Strategies: {orchestrator.migration_strategies}")
    print(f"Average Project Cost: ${projects['estimated_cost_usd'].mean():,.2f}")

