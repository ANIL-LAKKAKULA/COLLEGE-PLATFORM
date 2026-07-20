"""
Relation_Models: UserRole, RolePermission
"""

from ..core.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"


class RolePermission(Base):
    __tablename__ = "role_permissions"
