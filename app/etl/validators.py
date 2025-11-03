import re
import logging
from typing import Dict, Any
from datetime import datetime
from uuid import UUID

logger = logging.getLogger(__name__)

UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")

class BaseValidator:
    def validate(self, row: Dict[str, Any]) -> (bool, str):
        """Возвращает (is_valid, error_message)"""
        raise NotImplementedError

    def _is_uuid(self, value) -> bool:
        if not value:
            return False
        if isinstance(value, UUID):
            return True
        if isinstance(value, str):
            return bool(UUID_PATTERN.match(value))
        return False

    def _is_date(self, value) -> bool:
        if not value:
            return False
        if isinstance(value, datetime):
            return True
        try:
            datetime.fromisoformat(str(value))
            return True
        except Exception:
            return False

    def _is_positive(self, value) -> bool:
        try:
            return float(value) >= 0
        except Exception:
            return False


# ---------------- USERS ----------------
class UserValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        # Проверка обязательных
        if not row.get("email") and not row.get("user_id"):
            return False, "User missing both email and user_id"

        # Проверка email
        if row.get("email") and not EMAIL_PATTERN.match(str(row["email"])):
            return False, f"Invalid email format: {row['email']}"

        # Проверка user_id
        if row.get("user_id") and not self._is_uuid(row["user_id"]):
            return False, f"Invalid UUID for user_id: {row['user_id']}"

        # Проверка телефона
        if row.get("phone") and not PHONE_PATTERN.match(str(row["phone"])):
            return False, f"Invalid phone number: {row['phone']}"

        # Проверка даты регистрации
        if row.get("registration_date") and not self._is_date(row["registration_date"]):
            return False, f"Invalid registration_date: {row['registration_date']}"

        return True, ""


# ---------------- SCOOTERS ----------------
class ScooterValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        if not row.get("scooter_id"):
            return False, "Missing scooter_id"
        if not self._is_uuid(row["scooter_id"]):
            return False, f"Invalid scooter_id UUID: {row['scooter_id']}"

        if not row.get("model"):
            return False, "Missing model for scooter"

        # battery_level — от 0 до 100
        if row.get("battery_level") is not None:
            try:
                b = float(row["battery_level"])
                if b < 0 or b > 100:
                    return False, f"Battery level out of range (0-100): {b}"
            except ValueError:
                return False, f"Invalid battery_level value: {row['battery_level']}"

        # last_service_date — должна быть датой, не в будущем
        if row.get("last_service_date"):
            if not self._is_date(row["last_service_date"]):
                return False, f"Invalid last_service_date: {row['last_service_date']}"
            d = datetime.fromisoformat(str(row["last_service_date"]))
            if d > datetime.now():
                return False, f"Future last_service_date not allowed: {row['last_service_date']}"

        # status
        if not row.get("status"):
            return False, "Missing status"
        allowed_status = {"available", "in_use", "maintenance", "reserved", "offline"}
        if str(row["status"]).lower() not in allowed_status:
            return False, f"Invalid scooter status: {row['status']}"

        return True, ""


# ---------------- TARIFFS ----------------
class TariffValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        if not row.get("tariff_id"):
            return False, "Missing tariff_id"
        if not self._is_uuid(row["tariff_id"]):
            return False, f"Invalid UUID for tariff_id: {row['tariff_id']}"

        if not row.get("name"):
            return False, "Missing tariff name"

        # Цена должна быть положительной
        if not self._is_positive(row.get("price_per_minute", 0)):
            return False, f"Invalid price_per_minute: {row.get('price_per_minute')}"

        return True, ""


# ---------------- RIDES ----------------
class RideValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        for field in ("ride_id", "user_id", "scooter_id"):
            if not row.get(field):
                return False, f"Missing required field {field}"
            if not self._is_uuid(row[field]):
                return False, f"Invalid UUID for {field}: {row[field]}"

        # Проверка дат
        if not row.get("start_ts") or not self._is_date(row["start_ts"]):
            return False, f"Invalid start_ts: {row.get('start_ts')}"
        if not row.get("end_ts") or not self._is_date(row["end_ts"]):
            return False, f"Invalid end_ts: {row.get('end_ts')}"

        start = datetime.fromisoformat(str(row["start_ts"]))
        end = datetime.fromisoformat(str(row["end_ts"]))
        if end < start:
            return False, "end_ts is before start_ts"

        # Проверка дистанции и продолжительности
        if row.get("duration_seconds") is not None:
            if not self._is_positive(row["duration_seconds"]):
                return False, f"Negative duration_seconds: {row['duration_seconds']}"
        if row.get("distance_meters") is not None:
            if not self._is_positive(row["distance_meters"]):
                return False, f"Negative distance_meters: {row['distance_meters']}"

        return True, ""


# ---------------- PAYMENTS ----------------
class PaymentValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        if not row.get("payment_id"):
            return False, "Missing payment_id"
        if not self._is_uuid(row["payment_id"]):
            return False, f"Invalid UUID for payment_id: {row['payment_id']}"

        if not row.get("amount"):
            return False, "Missing amount"
        if not self._is_positive(row["amount"]):
            return False, f"Invalid payment amount: {row['amount']}"

        if row.get("status"):
            allowed = {"paid", "pending", "failed", "refunded"}
            if str(row["status"]).lower() not in allowed:
                return False, f"Invalid payment status: {row['status']}"

        if row.get("payment_date") and not self._is_date(row["payment_date"]):
            return False, f"Invalid payment_date: {row['payment_date']}"

        return True, ""


# ---------------- MAINTENANCE ----------------
class MaintenanceValidator(BaseValidator):
    def validate(self, row: Dict[str, Any]):
        if not row.get("maintenance_id"):
            return False, "Missing maintenance_id"
        if not self._is_uuid(row["maintenance_id"]):
            return False, f"Invalid UUID for maintenance_id: {row['maintenance_id']}"

        if not row.get("scooter_id"):
            return False, "Missing scooter_id"
        if not self._is_uuid(row["scooter_id"]):
            return False, f"Invalid UUID for scooter_id: {row['scooter_id']}"

        if not row.get("service_type"):
            return False, "Missing service_type"

        if row.get("service_date") and not self._is_date(row["service_date"]):
            return False, f"Invalid service_date: {row['service_date']}"

        return True, ""
