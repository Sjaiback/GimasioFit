from django.db import migrations


def seed_superuser_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    StaffProfile = apps.get_model("accounts", "StaffProfile")
    for user in User.objects.filter(is_superuser=True):
        StaffProfile.objects.update_or_create(
            user=user,
            defaults={"role": "admin", "is_active": True},
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(seed_superuser_profiles, noop),
    ]
