def attendance_record_to_dict(record):
    return {
        "id": record.id,
        "member_id": record.member_id,
        "member": str(record.member),
        "check_in_at": record.check_in_at.isoformat(),
        "check_out_at": record.check_out_at.isoformat() if record.check_out_at else None,
        "source": record.source,
        "is_open": record.is_open,
        "duration_minutes": record.duration_minutes,
    }
