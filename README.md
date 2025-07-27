# Cloud Optimization Dashboard

A full-stack application for monitoring cloud resources and discovering cost optimization opportunities. The backend is built with FastAPI and PostgreSQL, and the frontend uses Next.js and React.

---

## 🚀 Feature Overview

- **Dashboard**: Visual summary of total resources, monthly cost, potential savings, and optimization opportunities.
- **Resource List**: View all cloud resources with utilization metrics (CPU, memory, storage, cost).
- **Optimization Recommendations**: AI-driven suggestions for downsizing or optimizing resources to save costs.
- **Mark Recommendations as Implemented**: Track which optimizations have been applied.
- **Responsive UI**: Modern, responsive design with real-time feedback and notifications.

> **Sample Dashboard UI:**
>
> ![Dashboard Screenshot](docs/dashboard-screenshot.png)

---

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL database (or use the provided NeonDB connection)

### 1. Backend Setup

We use [uv](https://github.com/astral-sh/uv) for fast Python dependency management.

**Install dependencies:**
```sh
cd backend
uv sync --locked
```

- Copy `.env` and update with your database credentials if needed.
- Run database migrations and seed sample data automatically on startup.

**Start the backend:**

```sh
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at [http://localhost:8000](http://localhost:8000).

### 2. Frontend Setup

```sh
cd cloud-optimizer-frontend
npm install
npm run dev
```

Frontend will be available at [http://localhost:3000](http://localhost:3000).

---

## 🗃️ Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database schema migrations. Migrations are automatically run on application startup, but you can also manage them manually.

### Environment Variables

Ensure your `.env` file contains the database connection details:

```env
# Option 1: Full DATABASE_URL (recommended)
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require

# Option 2: Individual components (fallback)
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_PORT=5432
POSTGRES_DB=your_database
```

### Manual Migration Commands

**Initialize Alembic (already done):**
```sh
cd backend
uv run alembic init alembic
```

**Create a new migration:**
```sh
# After making changes to models.py
uv run alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**
```sh
# Apply all pending migrations
uv run alembic upgrade head

# Apply migrations up to a specific revision
uv run alembic upgrade <revision_id>

# Rollback to previous migration
uv run alembic downgrade -1

# Rollback to specific revision
uv run alembic downgrade <revision_id>
```

**View migration history:**
```sh
# Show current migration status
uv run alembic current

# Show migration history
uv run alembic history

# Show pending migrations
uv run alembic show <revision_id>
```

### Migration Workflow

1. **Make changes to your models** in `app/models.py`
2. **Generate migration script:**
   ```sh
   uv run alembic revision --autogenerate -m "Add new column to resources table"
   ```
3. **Review the generated migration** in `alembic/versions/`
4. **Apply the migration:**
   ```sh
   uv run alembic upgrade head
   ```

### Example Migration Scenarios

**Adding a new column:**
```python
# In app/models.py
class Resource(Base):
    __tablename__ = "resources"
    
    # ... existing columns ...
    region = Column(String)  # New column
```

Then run:
```sh
uv run alembic revision --autogenerate -m "Add region column to resources"
uv run alembic upgrade head
```

**Modifying existing column:**
```python
# In app/models.py
class Resource(Base):
    __tablename__ = "resources"
    
    # ... existing columns ...
    monthly_cost = Column(Float, nullable=False)  # Changed from nullable=True
```

**Creating new table:**
```python
# In app/models.py
class OptimizationHistory(Base):
    __tablename__ = "optimization_history"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    recommendation_type = Column(String)
    implemented_at = Column(DateTime, default=datetime.utcnow)
    savings_achieved = Column(Float)
```

### Troubleshooting Migrations

**Reset database (development only):**
```sh
# Drop all tables and recreate from scratch
uv run python -c "
from app.database import engine
from app.models import Base
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
"

# Then mark as current migration
uv run alembic stamp head
```

**Fix migration conflicts:**
```sh
# If migrations are out of sync, you can resolve conflicts by:
# 1. Check current database state
uv run alembic current

# 2. Manually resolve conflicts in migration files
# 3. Mark specific revision as current
uv run alembic stamp <revision_id>

# 4. Continue with normal migration process
uv run alembic upgrade head
```

**Common Issues:**

- **"Can't locate revision"**: Check that `alembic/versions/` contains migration files
- **"Database connection failed"**: Verify your `.env` database credentials
- **"SSL connection required"**: Ensure `?sslmode=require` is in your DATABASE_URL for cloud databases
- **"Target database is not up to date"**: Run `uv run alembic upgrade head`

### Production Deployment

For production deployments:

1. **Run migrations before starting the application:**
   ```sh
   uv run alembic upgrade head
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Or disable auto-migration** by commenting out the migration code in `main.py`:
   ```python
   # @app.on_event("startup")
   # async def startup_event():
   #     # Disable auto-migration in production
   #     pass
   ```

---

## 📖 API Documentation

### Base URL

- Local: `http://localhost:8000`

### Endpoints

#### `GET /resources`

- **Description:** Returns a list of all cloud resources.
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "name": "web-server-1",
      "resource_type": "compute",
      "provider": "AWS",
      "instance_type": "t3.xlarge",
      "cpu_utilization": 15.0,
      "memory_utilization": 25.0,
      "storage_gb": 100.0,
      "monthly_cost": 150.0,
      "created_at": "2024-07-27T12:00:00"
    }
  ]
  ```

#### `GET /recommendations`

- **Description:** Returns optimization recommendations for resources.
- **Response Example:**
  ```json
  [
    {
      "resource_id": 1,
      "resource_name": "web-server-1",
      "type": "downsize_instance",
      "current_config": "t3.xlarge - 15.0% CPU, 25.0% Memory",
      "recommended_config": "Smaller instance type (50% less resources)",
      "reasoning": "Low utilization detected: 15.0% CPU, 25.0% Memory",
      "monthly_savings": 75.0,
      "confidence": "High"
    }
  ]
  ```

#### `GET /summary`

- **Description:** Returns a summary of resources, costs, and savings.
- **Response Example:**
  ```json
  {
    "total_resources": 8,
    "total_monthly_cost": 740.0,
    "total_potential_savings": 150.0,
    "optimization_opportunities": 2
  }
  ```

#### `GET /health`

- **Description:** Health check endpoint.
- **Response Example:**
  ```json
  {
    "status": "healthy",
    "message": "API is running properly"
  }
  ```

---

## 🗄️ Database Schema

**Table: `resources`**

| Column              | Type      | Description                        |
|---------------------|-----------|------------------------------------|
| id                  | Integer   | Primary key                        |
| name                | String    | Unique resource name               |
| resource_type       | String    | 'compute' or 'storage'             |
| provider            | String    | 'AWS', 'Azure', 'GCP', etc.        |
| instance_type       | String    | Instance or storage type           |
| cpu_utilization     | Float     | CPU usage (%)                      |
| memory_utilization  | Float     | Memory usage (%)                   |
| storage_gb          | Float     | Storage size in GB                 |
| monthly_cost        | Float     | Monthly cost in USD                |
| created_at          | DateTime  | Creation timestamp                 |

- **Indexes:** Unique on `name`, index on `id`.

> **Note:** All recommendations are generated dynamically based on resource utilization and cost.

---

## 📝 How Recommendations Work

- **Downsize Compute:** If both CPU < 30% and Memory < 50%, a recommendation to downsize is generated.
- **Optimize Storage:** If storage > 500GB, a recommendation to reduce storage is generated.
- **Potential savings** are calculated as a percentage of the current monthly cost.

---

## 📦 Project Structure

```
backend/
  app/
    main.py         # FastAPI entrypoint
    models.py       # SQLAlchemy models
    crud.py         # Database and recommendation logic
    database.py     # DB connection/session
  alembic/          # Database migrations
    versions/       # Migration scripts
    env.py          # Alembic environment config
  alembic.ini       # Alembic configuration
  .env              # Database credentials

cloud-optimizer-frontend/
  src/
    app/
      page.tsx      # Main dashboard UI
    components/ui/  # Reusable UI components
    lib/utils.ts    # Utility functions
  public/           # Static assets
```

---

## 🤝 Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

When contributing database schema changes:

1. Make your changes to `app/models.py`
2. Generate a migration: `uv run alembic revision --autogenerate -m "Description"`
3. Review and test the migration
4. Include the migration file in your pull request

---

## 📄 License

This project is licensed under the Apache License 2.0.

---
