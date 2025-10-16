from fastapi import HTTPException, status
from requests import Session
from repositories.database_repository import DatabaseRepository
from schemas.database import DatabaseCreate
from schemas.database_schema import ColumnExport, DatabaseInfoExport, DatabaseSchemaExport, ForeignKeyExport, IndexExport, RelationshipExport, TableDetailExport
from services.table_service import table_service
from services.column_service import column_service
from services.foreign_key_service import foreign_key_service
from services.index_service import index_service
from services.relationship_service import relationship_service
from services.base_service import BaseService

class DatabaseService(BaseService):
    def __init__(self):
        super().__init__(DatabaseRepository)

    def validate_fields(self, database: DatabaseCreate):
        required_fields = {
            "engine": "Tipo de banco é obrigatório",
            "version": "Versão é obrigatório",
            "hostname": "Servidor é obrigatório",
            "database": "Banco de daoos é obrigatório",
            "username": "Usuário é obrigatório",
            "password": "Senha é obrigatório",
        }

        for field, message in required_fields.items():
            value = getattr(database, field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
            
        allowed_types = ['MYSQL', 'SQLSERVER', 'POSTGRES']
        if database.engine.upper() not in allowed_types:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de banco inválido")
        
        return database
    
    def get_database_schema_json(self, db: Session, database_id: int) -> DatabaseSchemaExport:
        db_database = self.get(db, database_id)
        if not db_database:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Database not found")

        tables_data = {}
        tables = table_service.get_by_database_id(db, database_id)
        for tbl in tables:
            columns_data = {}
            columns = column_service.get_by_table_id(db, tbl.id)
            for col in columns:
                foreign_key_data = None
                fk = foreign_key_service.get_by_column_id(db, col.id)
                if fk:
                    foreign_key_data = ForeignKeyExport(
                        references_table=fk[0].references_table,
                        references_column=fk[0].references_column,
                        on_delete=fk[0].on_delete,
                        on_update=fk[0].on_update
                    )
                columns_data[col.name] = ColumnExport(
                    type=col.type,
                    size=col.size,
                    nullable=col.nullable,
                    auto_increment=col.auto_increment,
                    primary_key=col.primary_key,
                    description=col.description,
                    foreign_key=foreign_key_data
                )
            
            indexes_list = []
            indexes = index_service.get_by_table_id(db, tbl.id)
            for idx in indexes:
                indexes_list.append(IndexExport(
                    name=idx.name,
                    type=idx.type,
                    columns=idx.columns.split(',') if idx.columns else [] # Assuming columns are stored as comma-separated string
                ))
            
            tables_data[tbl.name] = TableDetailExport(
                description=tbl.description,
                columns=columns_data,
                indexes=indexes_list
            )

        relationships_list = []
        relationships = relationship_service.get_by_database_id(db, database_id)
        for rel in relationships:
            relationships_list.append(RelationshipExport(
                type=rel.type,
                parent=rel.parent,
                child=rel.child,
                description=rel.description
            ))

        database_info = DatabaseInfoExport(
            name=db_database.database,
            engine=db_database.engine,
            version=db_database.version,
            charset=db_database.charset
        )

        return DatabaseSchemaExport(
            database=database_info,
            tables=tables_data,
            relationships=relationships_list
        )
    
database_service = DatabaseService()
