import asyncio
from database import init_db, get_db, close_db
from models import AdminUser
from auth import get_password_hash

async def create_admin():
    await init_db()
    async for db in get_db():
        existing_admin = await db.execute(
            AdminUser.__table__.select().where(AdminUser.username == "admin")
        )
        if existing_admin.scalar():
            print("👤 Admin déjà existant")
        else:
            admin = AdminUser(
                username="admin",
                hashed_password=get_password_hash("admin123")
            )
            db.add(admin)
            await db.commit()
            print("✅ Admin créé avec succès : admin / admin123")
    await close_db()

if __name__ == "__main__":
    asyncio.run(create_admin())
