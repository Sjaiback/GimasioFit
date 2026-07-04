def plan_to_dict(plan):
    return {
        "id": plan.id,
        "name": plan.name,
        "duration_months": plan.duration_months,
        "price": str(plan.price),
        "description": plan.description,
        "is_active": plan.is_active,
    }


def membership_to_dict(membership):
    return {
        "id": membership.id,
        "member_id": membership.member_id,
        "member": str(membership.member),
        "plan_id": membership.plan_id,
        "plan": membership.plan.name,
        "start_date": membership.start_date.isoformat(),
        "end_date": membership.end_date.isoformat(),
        "status": membership.status,
        "days_to_expire": membership.days_to_expire,
        "renewal_count": membership.renewal_count,
    }
