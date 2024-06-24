from typing import Tuple, Dict
from database.database import DATABASE_DRIVER_NAME


class BaseIntegrityErrorMessageParser:
    def __init__(self):
        self.error_message_key: Dict[str, str] = {}

    def parsing(self, integrity_error_message: str) -> Tuple[str, str, str]:
        return ("unknown", "unknown", "unknown")


class SQLiteIntegrityErrorMessageParser(BaseIntegrityErrorMessageParser):
    def __init__(self):
        super().__init__()
        self.error_message_key["UNIQUE constraint failed"] = "unique"
        self.error_message_key["NOT NULL constraint failed"] = "not_null"
        self.error_message_key["FOREIGN KEY constraint failed"] = "foreign_key"

    def parsing(self, integrity_error_message: str) -> Tuple[str, str, str]:
        error_message = "unknown"
        table_name = "unknown"
        column_name = "unknown"
        error_type = "unknown"

        splited_integrity_error_message = integrity_error_message.split(":")

        if len(splited_integrity_error_message) == 2:
            error_message = splited_integrity_error_message[0]

        if error_message in self.error_message_key:
            error_type = self.error_message_key.get(error_message, "unknown")

            splited_residual_message = splited_integrity_error_message[-1].split(".")

            if len(splited_residual_message) == 2 and error_type != "unknown":
                table_name = splited_residual_message[0]
                column_name = splited_residual_message[-1]

        return (error_type, table_name, column_name)


class IntegrityErrorMessageParser:
    def __init__(self):
        self.parser: Dict[str, BaseIntegrityErrorMessageParser] = {
            "sqlite": SQLiteIntegrityErrorMessageParser()
        }

    def parsing(
        self,
        integrity_error_message_orig: str,
        data_base_driver_name: str = DATABASE_DRIVER_NAME,
    ) -> Tuple[str, str, str]:
        if data_base_driver_name in self.parser:
            return self.parser.get(data_base_driver_name).parsing(
                integrity_error_message=str(integrity_error_message_orig)
            )
        else:
            return ("unknown", "unknown", "unknown")


intergrity_error_message_parser = IntegrityErrorMessageParser()
