from typing import List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import asc, desc, select, func
from sqlalchemy.orm import Session

from . import models, schemas


def get_bird_or_404(db: Session, bird_id: int) -> models.Bird:
	bird = db.get(models.Bird, bird_id)
	if bird is None:
		raise HTTPException(status_code=404, detail="Bird not found")
	return bird


def list_birds(
	db: Session,
	search: Optional[str] = None,
	species: Optional[str] = None,
	skip: int = 0,
	limit: int = 50,
	sort_by: str = "name",
	sort_dir: str = "asc",
) -> Tuple[List[models.Bird], int]:
	base_query = select(models.Bird)

	if search:
		like = f"%{search.lower()}%"
		base_query = base_query.where(
			(models.Bird.name.ilike(like)) | (models.Bird.species.ilike(like))
		)

	if species:
		base_query = base_query.where(models.Bird.species == species)

	# Total count for the filtered query
	total = db.execute(
		select(func.count())
		.select_from(base_query.subquery())
	).scalar_one()

	# Sorting and pagination applied after counting
	sort_column = getattr(models.Bird, sort_by, None)
	if sort_column is None:
		sort_column = models.Bird.name
	order_func = asc if sort_dir.lower() == "asc" else desc

	data_query = base_query.order_by(order_func(sort_column)).offset(max(skip, 0)).limit(max(limit, 1))

	birds = db.execute(data_query).scalars().all()
	return birds, total


def create_bird(db: Session, payload: schemas.BirdCreate) -> models.Bird:
	bird = models.Bird(
		name=payload.name,
		species=payload.species,
		price=payload.price,
		in_stock=payload.in_stock,
		description=payload.description,
	)
	db.add(bird)
	db.commit()
	db.refresh(bird)
	return bird


def update_bird(db: Session, bird_id: int, payload: schemas.BirdUpdate) -> models.Bird:
	bird = get_bird_or_404(db, bird_id)
	for field_name, value in payload.model_dump(exclude_unset=True).items():
		setattr(bird, field_name, value)
	db.add(bird)
	db.commit()
	db.refresh(bird)
	return bird


def delete_bird(db: Session, bird_id: int) -> None:
	bird = get_bird_or_404(db, bird_id)
	db.delete(bird)
	db.commit()