"""
Base_Models: User, Role, Permission
"""

from ..core.database import Base


class User(Base):
    __tablename__ = "users"


class Role(Base):
    __tablename__ = "roles"


class Permission(Base):
    __tablename__ = "permissions"
