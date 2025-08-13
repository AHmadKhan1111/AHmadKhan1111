from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from . import crud, models, schemas


app = FastAPI(title="Birds Store API", version="0.1.0")

# Allow all origins for simplicity; tighten in production
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Database session dependency

def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# Create tables on startup
@app.on_event("startup")
def on_startup() -> None:
	# Ensure models are imported so metadata is aware
	Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> Dict[str, str]:
	return {"status": "ok"}


@app.get("/birds", response_model=schemas.BirdListResponse)
def list_birds(
	search: Optional[str] = Query(default=None, description="Search by name or species"),
	species: Optional[str] = Query(default=None, description="Filter by exact species"),
	skip: int = Query(default=0, ge=0),
	limit: int = Query(default=50, ge=1, le=500),
	sort_by: str = Query(default="name"),
	sort_dir: str = Query(default="asc"),
	db: Session = Depends(get_db),
) -> schemas.BirdListResponse:
	items, total = crud.list_birds(
		db=db,
		search=search,
		species=species,
		skip=skip,
		limit=limit,
		sort_by=sort_by,
		sort_dir=sort_dir,
	)
	return schemas.BirdListResponse(items=items, total=total)


@app.get("/birds/{bird_id}", response_model=schemas.BirdOut)
def get_bird(bird_id: int, db: Session = Depends(get_db)) -> schemas.BirdOut:
	bird = crud.get_bird_or_404(db, bird_id)
	return bird


@app.post("/birds", response_model=schemas.BirdOut, status_code=status.HTTP_201_CREATED)
def create_bird(payload: schemas.BirdCreate, db: Session = Depends(get_db)) -> schemas.BirdOut:
	return crud.create_bird(db, payload)


@app.patch("/birds/{bird_id}", response_model=schemas.BirdOut)
def update_bird(bird_id: int, payload: schemas.BirdUpdate, db: Session = Depends(get_db)) -> schemas.BirdOut:
	return crud.update_bird(db, bird_id, payload)


@app.delete("/birds/{bird_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bird(bird_id: int, db: Session = Depends(get_db)) -> None:
	crud.delete_bird(db, bird_id)
	return None


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("birds_store.main:app", host="0.0.0.0", port=8000, reload=False)