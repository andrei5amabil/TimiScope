from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert

from app.db.session import SessionLocal
from app.models import Category


CATEGORIES = [
    {
        "name": "Infrastructure",
        "description": "Roads, sidewalks, streetlights and public infrastructure.",
    },
    {
        "name": "Mobility & Transport",
        "description": "Traffic, cycling, accessibility and transportation.",
    },
    {
        "name": "Environment",
        "description": "Waste, pollution, flooding and environmental observations.",
    },
    {
        "name": "Public Spaces",
        "description": "Parks, public facilities and accessibility.",
    },
    {
        "name": "Community & Events",
        "description": "Concerts, festivals, markets and community activities.",
    },
    {
        "name": "Food & Drink",
        "description": "Restaurants, cafes and food-related activities.",
    },
    {
        "name": "Education & Culture",
        "description": "Educational and cultural activities.",
    },
]


def seed_categories() -> None:
    """Insert predefined categories without creating duplicates."""

    values = [
        {
            "id": uuid4(),
            "name": category["name"],
            "description": category["description"],
            "is_active": True,
        }
        for category in CATEGORIES
    ]

    statement = (
        insert(Category)
        .values(values)
        .on_conflict_do_nothing(
            index_elements=[Category.name]
        )
    )

    with SessionLocal.begin() as session:
        result = session.execute(statement)
        inserted_count = result.rowcount or 0

    print(
        f"Category seeding completed. "
        f"Inserted {inserted_count} new categories."
    )


if __name__ == "__main__":
    seed_categories()