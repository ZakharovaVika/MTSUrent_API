import re
from uuid import UUID
from datetime import datetime, date
from typing import Any, Dict, Optional


def to_uuid(value: Any) -> Optional[str]:
    """Проверка UUID."""
    try:
        return str(UUID(str(value)))
    except Exception:
        return None


def to_date(value: Any) -> Optional[date]:
    """Преобразование строки в дату."""
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None


def to_datetime(value: Any) -> Optional[datetime]:
    """Преобразование строки в datetime."""
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d.%m.%Y %H:%M"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    return None


def normalize_phone(phone: str) -> Optional[str]:
    """Очистка и нормализация телефона."""
    if not phone:
        return None
    phone = re.sub(r"[^\d+]", "", phone)
    if not phone.startswith("+"):
        phone = "+" + phone
    return phone if len(phone) >= 10 else None


class DataTransformer:
    """ETL-трансформеры под схемы MTSUrent."""

    # === USERS ===
    def transform_users(self, row: Dict[str, Any]) -> Dict[str, Any]:
        out = {}

        out["user_id"] = to_uuid(row.get("user_id") or row.get("id"))
        full_name = (row.get("full_name") or row.get("name") or "").strip()
        if full_name:
            parts = full_name.split()
            out["first_name"] = parts[0]
            out["last_name"] = " ".join(parts[1:]) if len(parts) > 1 else "—"
        else:
            out["first_name"] = "—"
            out["last_name"] = "—"

        out["email"] = row.get("email") or None
        out["phone_number"] = normalize_phone(row.get("phone") or row.get("phone_number"))
        out["date_of_birth"] = to_date(row.get("date_of_birth"))
        out["registration_date"] = to_datetime(row.get("registration_date")) or datetime.now()
        out["rating"] = float(row.get("rating") or 0)
        return out

    # === SCOOTERS ===
    def transform_scooters(self, row: Dict[str, Any]) -> Dict[str, Any]:
        out = {}
        out["scooter_id"] = to_uuid(row.get("scooter_id") or row.get("id"))
        out["model"] = row.get("model")
        out["manufacture_date"] = to_date(row.get("manufacture_date"))
        out["current_battery"] = int(row.get("current_battery") or 0)
        out["gps_latitude"] = float(row.get("gps_latitude") or 0)
        out["gps_longitude"] = float(row.get("gps_longitude") or 0)
        out["status_code"] = row.get("status_code")
        out["qr_code"] = row.get("qr_code") or ""
        return out


    # === TARIFFS ===
    def transform_tariffs(self, row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tariff_id": to_uuid(row.get("tariff_id") or row.get("id")),
            "tariff_name": row.get("tariff_name"),
            "unlock_fee": float(row.get("unlock_fee") or 0),
            "rate_per_minute": float(row.get("rate_per_minute") or 0),
            "rate_per_km": float(row.get("rate_per_km") or 0),
            "is_active": str(row.get("is_active")).lower() in ["true", "1", "yes"],
            "created_datetime": to_datetime(row.get("created_datetime")) or datetime.now(),
        }


    # === RIDES ===
    def transform_rides(self, row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ride_id": to_uuid(row.get("ride_id") or row.get("id")),
            "user_id": to_uuid(row.get("user_id")),
            "scooter_id": to_uuid(row.get("scooter_id")),
            "tariff_id": to_uuid(row.get("tariff_id")),
            "start_latitude": float(row.get("start_latitude") or 0),
            "start_longitude": float(row.get("start_longitude") or 0),
            "end_latitude": float(row.get("end_latitude") or 0),
            "end_longitude": float(row.get("end_longitude") or 0),
            "distance": float(row.get("distance") or 0),
            "ride_cost": float(row.get("ride_cost") or 0),
            "start_time": to_datetime(row.get("start_time")) or datetime.now(),
            "end_time": to_datetime(row.get("end_time")),
            "created_datetime": to_datetime(row.get("created_datetime")) or datetime.now(),
        }
