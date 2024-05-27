# Generated by Django 4.2.13 on 2024-05-27 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0004_merge_0002_adding_fk_0003_adding_table'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE ai_usage (
                ai_usage_id SERIAL PRIMARY KEY,
                user_id int NOT NULL,
                todo_id int NOT NULL,
                usage_count int,
                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES "users" (user_id),
                FOREIGN KEY (todo_id) REFERENCES "todo" (todo_id)
            );
            """,
            reverse_sql="DROP TABLE ai_usage;"
        )

    ]
