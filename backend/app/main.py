from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from . import models, crud
from .database import get_database
import uvicorn

app = FastAPI(
    title="Cloud Optimization Dashboard API",
    description="API for cloud resource optimization recommendations",
    version="1.0.0"
)

# Updated CORS middleware for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.56.2:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models for responses
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResourceResponse(BaseModel):
    id: int
    name: str
    resource_type: str
    provider: str
    instance_type: str
    cpu_utilization: Optional[float]
    memory_utilization: Optional[float]
    storage_gb: Optional[float]
    monthly_cost: float
    created_at: datetime

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    resource_id: int
    resource_name: str
    type: str
    current_config: str
    recommended_config: str
    reasoning: str
    monthly_savings: float
    confidence: str

class SummaryResponse(BaseModel):
    total_resources: int
    total_monthly_cost: float
    total_potential_savings: float
    optimization_opportunities: int

@app.on_event("startup")
async def startup_event():
    # Run migrations automatically on startup (optional)
    import subprocess
    import sys
    from .database import engine
    
    try:
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                      cwd=".", check=True, capture_output=True)
        print("✅ Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Migration failed or Alembic not configured: {e}")
        print("🔄 Falling back to auto table creation...")
        # Fallback to current method if Alembic isn't set up
        models.Base.metadata.create_all(bind=engine)
    except FileNotFoundError:
        print("⚠️ Alembic not found - using table auto-creation")
        # Fallback to current method if Alembic isn't set up
        models.Base.metadata.create_all(bind=engine)
    
    # Seed data after migrations/table creation
    db = next(get_database())
    crud.seed_sample_data(db)

@app.get("/")
async def root():
    return {"message": "Cloud Optimization Dashboard API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}

@app.get("/resources", response_model=List[ResourceResponse])
async def get_resources(db: Session = Depends(get_database)):
    try:
        resources = crud.get_resources(db)
        print(f"📊 Returning {len(resources)} resources")
        return resources
    except Exception as e:
        print(f"❌ Error fetching resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(db: Session = Depends(get_database)):
    try:
        recommendations = crud.generate_recommendations(db)
        print(f"💡 Returning {len(recommendations)} recommendations")
        return recommendations
    except Exception as e:
        print(f"❌ Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary", response_model=SummaryResponse)
async def get_summary(db: Session = Depends(get_database)):
    try:
        resources = crud.get_resources(db)
        recommendations = crud.generate_recommendations(db)
        
        total_resources = len(resources)
        total_monthly_cost = sum(resource.monthly_cost for resource in resources)
        total_potential_savings = sum(rec["monthly_savings"] for rec in recommendations)
        optimization_opportunities = len(recommendations)
        
        summary = SummaryResponse(
            total_resources=total_resources,
            total_monthly_cost=round(total_monthly_cost, 2),
            total_potential_savings=round(total_potential_savings, 2),
            optimization_opportunities=optimization_opportunities
        )
        
        print(f"📈 Summary: {total_resources} resources, ${total_monthly_cost} cost, ${total_potential_savings} savings")
        return summary
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)