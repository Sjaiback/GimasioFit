def member_to_dict(member):
    return {
        "id": member.id,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "full_name": str(member),
        "document_number": member.document_number,
        "birth_date": member.birth_date.isoformat() if member.birth_date else None,
        "phone": member.phone,
        "email": member.email,
        "address": member.address,
        "emergency_contact": member.emergency_contact,
        "emergency_phone": member.emergency_phone,
        "status": member.status,
        "notes": member.notes,
        "joined_at": member.joined_at.isoformat(),
        "updated_at": member.updated_at.isoformat(),
    }
