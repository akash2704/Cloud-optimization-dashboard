from sqlalchemy.orm import Session
from . import models
from typing import List, Dict, Any

def get_resources(db: Session) -> List[models.Resource]:
    return db.query(models.Resource).all()

def create_resource(db: Session, resource_data: dict) -> models.Resource:
    db_resource = models.Resource(**resource_data)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def seed_sample_data(db: Session):
    # Check if data already exists
    if db.query(models.Resource).count() > 0:
        return
    
    sample_resources = [
        {
            "name": "web-server-1",
            "resource_type": "compute",
            "provider": "AWS",
            "instance_type": "t3.xlarge",
            "cpu_utilization": 15.0,
            "memory_utilization": 25.0,
            "storage_gb": 100.0,
            "monthly_cost": 150.0
        },
        {
            "name": "api-server-2",
            "resource_type": "compute",
            "provider": "AWS",
            "instance_type": "m5.large",
            "cpu_utilization": 12.0,
            "memory_utilization": 30.0,
            "storage_gb": 50.0,
            "monthly_cost": 90.0
        },
        {
            "name": "worker-3",
            "resource_type": "compute",
            "provider": "Azure",
            "instance_type": "Standard_D2s_v3",
            "cpu_utilization": 8.0,
            "memory_utilization": 20.0,
            "storage_gb": 75.0,
            "monthly_cost": 70.0
        },
        {
            "name": "database-1",
            "resource_type": "compute",
            "provider": "AWS",
            "instance_type": "m5.xlarge",
            "cpu_utilization": 75.0,
            "memory_utilization": 85.0,
            "storage_gb": 200.0,
            "monthly_cost": 180.0
        },
        {
            "name": "cache-server",
            "resource_type": "compute",
            "provider": "GCP",
            "instance_type": "n1-standard-2",
            "cpu_utilization": 65.0,
            "memory_utilization": 70.0,
            "storage_gb": 30.0,
            "monthly_cost": 50.0
        },
        {
            "name": "backup-storage",
            "resource_type": "storage",
            "provider": "AWS",
            "instance_type": "S3 Standard",
            "cpu_utilization": None,
            "memory_utilization": None,
            "storage_gb": 1000.0,
            "monthly_cost": 100.0
        },
        {
            "name": "log-storage",
            "resource_type": "storage",
            "provider": "GCP",
            "instance_type": "Cloud Storage",
            "cpu_utilization": None,
            "memory_utilization": None,
            "storage_gb": 500.0,
            "monthly_cost": 75.0
        },
        {
            "name": "database-storage",
            "resource_type": "storage",
            "provider": "AWS",
            "instance_type": "EBS GP3",
            "cpu_utilization": None,
            "memory_utilization": None,
            "storage_gb": 200.0,
            "monthly_cost": 25.0
        }
    ]
    
    for resource_data in sample_resources:
        create_resource(db, resource_data)

def generate_recommendations(db: Session) -> List[Dict[str, Any]]:
    resources = get_resources(db)
    recommendations = []
    
    for resource in resources:
        # Over-provisioned compute instances
        if (resource.resource_type == "compute" and 
            resource.cpu_utilization is not None and 
            resource.memory_utilization is not None and
            resource.cpu_utilization < 30 and 
            resource.memory_utilization < 50):
            
            # Suggest downsizing with 50% cost savings
            savings = resource.monthly_cost * 0.5
            recommendations.append({
                "resource_id": resource.id,
                "resource_name": resource.name,
                "type": "downsize_instance",
                "current_config": f"{resource.instance_type} - {resource.cpu_utilization}% CPU, {resource.memory_utilization}% Memory",
                "recommended_config": "Smaller instance type (50% less resources)",
                "reasoning": f"Low utilization detected: {resource.cpu_utilization}% CPU, {resource.memory_utilization}% Memory",
                "monthly_savings": round(savings, 2),
                "confidence": "High" if savings > 50 else "Medium"
            })
        
        # Large storage optimization
        if (resource.resource_type == "storage" and 
            resource.storage_gb is not None and 
            resource.storage_gb > 500):
            
            # Suggest storage reduction with 30% cost savings
            savings = resource.monthly_cost * 0.3
            recommendations.append({
                "resource_id": resource.id,
                "resource_name": resource.name,
                "type": "optimize_storage",
                "current_config": f"{resource.storage_gb}GB {resource.instance_type}",
                "recommended_config": f"{int(resource.storage_gb * 0.7)}GB {resource.instance_type}",
                "reasoning": f"Large storage volume detected: {resource.storage_gb}GB",
                "monthly_savings": round(savings, 2),
                "confidence": "Medium"
            })
    
    return recommendations