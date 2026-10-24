from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Ad
from app.schemas import AdResponse, CreateAdRequest, UpdateAdRequest

router = APIRouter(tags=["advertisement"])


@router.post("", response_model=AdResponse, status_code=status.HTTP_201_CREATED)
async def create_ad(body: CreateAdRequest, db: AsyncSession = Depends(get_db)):
    ad = Ad(
        title=body.title,
        description=body.description,
        price=body.price,
        author=body.author,
        created_at=datetime.now(timezone.utc),
    )
    db.add(ad)
    await db.commit()
    await db.refresh(ad)
    return AdResponse(
        id=ad.id,
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
        created_at=ad.created_at,
    )


@router.get("/{ad_id}", response_model=AdResponse)
async def get_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return AdResponse(
        id=ad.id,
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
        created_at=ad.created_at,
    )


@router.patch("/{ad_id}", response_model=AdResponse)
async def update_ad(ad_id: int, body: UpdateAdRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    if body.title is not None:
        ad.title = body.title
    if body.description is not None:
        ad.description = body.description
    if body.price is not None:
        ad.price = body.price
    if body.author is not None:
        ad.author = body.author

    await db.commit()
    await db.refresh(ad)
    return AdResponse(
        id=ad.id,
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
        created_at=ad.created_at,
    )


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    await db.delete(ad)
    await db.commit()


@router.get("", response_model=list[AdResponse])
async def search_ads(
        title: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        price: Optional[float] = Query(None),
        author: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db),
):
    query = select(Ad)
    conditions = []

    if title:
        conditions.append(Ad.title.ilike(f"%{title}%"))
    if description:
        conditions.append(Ad.description.ilike(f"%{description}%"))
    if price:
        conditions.append(Ad.price == price)
    if author:
        conditions.append(Ad.author.ilike(f"%{author}%"))

    if conditions:
        query = query.where(*conditions)

    result = await db.execute(query)
    ads = result.scalars().all()
    return [
        AdResponse(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            price=ad.price,
            author=ad.author,
            created_at=ad.created_at,
        )
        for ad in ads
    ]
