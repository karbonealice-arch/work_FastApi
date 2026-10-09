import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from app.models import Ad
from app.schemas import CreateAdRequest, UpdateAdRequest

router = APIRouter(prefix="/advertisement", tags=["advertisement"])

# In-memory store: { id: { ...ad fields... } }
_ads_store: dict[str, dict] = {}


@router.post("", response_model=Ad, status_code=status.HTTP_201_CREATED)
def create_ad(body: CreateAdRequest):
    ad_id = str(uuid.uuid4())
    ad = {
        "id": ad_id,
        "title": body.title,
        "description": body.description,
        "price": body.price,
        "author": body.author,
        "created_at": datetime.now(timezone.utc),
    }
    _ads_store[ad_id] = ad
    return Ad(**ad)


@router.get("/{advertisement_id}", response_model=Ad)
def get_ad(advertisement_id: str):
    ad = _ads_store.get(advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return Ad(**ad)


@router.patch("/{advertisement_id}", response_model=Ad)
def update_ad(advertisement_id: str, body: UpdateAdRequest):
    ad = _ads_store.get(advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    if body.title is not None:
        ad["title"] = body.title
    if body.description is not None:
        ad["description"] = body.description
    if body.price is not None:
        ad["price"] = body.price
    if body.author is not None:
        ad["author"] = body.author
    return Ad(**ad)


@router.delete("/{advertisement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(advertisement_id: str):
    if advertisement_id not in _ads_store:
        raise HTTPException(status_code=404, detail="Ad not found")
    del _ads_store[advertisement_id]


@router.get("", response_model=list[Ad])
def search_ads(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
):
    results = list(_ads_store.values())
    if title:
        results = [a for a in results if title.lower() in a["title"].lower()]
    if author:
        results = [a for a in results if a["author"].lower() == author.lower()]
    return [Ad(**a) for a in results]
