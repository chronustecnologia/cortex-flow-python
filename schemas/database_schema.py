from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ForeignKeyExport(BaseModel):
    references_table: str
    references_column: str
    on_delete: Optional[str]
    on_update: Optional[str]

class ColumnExport(BaseModel):
    type: str
    size: Optional[int]
    nullable: bool
    auto_increment: bool
    primary_key: bool
    description: Optional[str]
    foreign_key: Optional[ForeignKeyExport]

class IndexExport(BaseModel):
    name: str
    type: str
    columns: List[str]

class TableDetailExport(BaseModel):
    description: Optional[str]
    columns: Dict[str, ColumnExport]
    indexes: List[IndexExport]

class DatabaseInfoExport(BaseModel):
    name: str
    engine: str
    version: str
    charset: Optional[str]

class RelationshipExport(BaseModel):
    type: str
    parent: str
    child: str
    description: Optional[str]

class DatabaseSchemaExport(BaseModel):
    database: DatabaseInfoExport
    tables: Dict[str, TableDetailExport]
    relationships: List[RelationshipExport]