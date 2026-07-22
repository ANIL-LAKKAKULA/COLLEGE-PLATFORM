"""Create the ADMIN role and first identity-service administrator.

Run after the schema migration from the identity service directory:

    python -m app.scripts.bootstrap_admin

The command is intentionally interactive so credentials are not passed in
shell history or committed to the repository. It creates the fixed ADMIN role
when it is missing, refuses to create a second user for an existing email, and
never prints the password.
"""

import asyncio
import getpass
from uuid import uuid4

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models import Role, User, UserRole
from sqlalchemy import select


def _required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This value is required.")


def _password() -> str:
    while True:
        password = getpass.getpass("Admin password: ")
        confirmation = getpass.getpass("Confirm password: ")
        if password != confirmation:
            print("Passwords do not match.")
        elif len(password) < 8:
            print("Password must contain at least 8 characters.")
        else:
            return password


async def bootstrap_admin() -> None:
    email = _required("Admin email: ").lower()
    full_name = _required("Full name: ")
    phone_number = _required("Phone number: ")
    password = _password()

    async with AsyncSessionLocal() as session:
        existing_user = await session.scalar(select(User).where(User.email == email))
        if existing_user is not None:
            raise SystemExit(f"A user with email {email} already exists.")

        admin_role = await session.scalar(select(Role).where(Role.name == "ADMIN"))
        if admin_role is None:
            admin_role = Role(id=uuid4(), name="ADMIN")
            session.add(admin_role)
            await session.flush()

        admin = User(
            id=uuid4(),
            email=email,
            full_name=full_name,
            password=hash_password(password),
            phone_number=phone_number,
            is_active=True,
        )
        session.add(admin)
        await session.flush()
        session.add(
            UserRole(
                id=uuid4(),
                user_id=admin.id,
                role_id=admin_role.id,
                assigned_by=None,
            )
        )
        await session.commit()

    print(f"Created ADMIN role and user: {email}")


if __name__ == "__main__":
    asyncio.run(bootstrap_admin())
