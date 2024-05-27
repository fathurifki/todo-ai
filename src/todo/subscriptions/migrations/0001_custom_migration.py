# Generated by Django 4.2.13 on 2024-05-26 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TYPE subscription_plan AS ENUM ('freemium', 'premium');
            CREATE TABLE IF NOT EXISTS subscription (
                subscription_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                plan subscription_plan NOT NULL DEFAULT 'freemium',
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                is_active BOOLEAN NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES "users" (user_id)
            );
            CREATE OR REPLACE FUNCTION create_freemium_subscription()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO subscription(user_id, plan, start_date, end_date, is_active, created_at, updated_at)
                VALUES (NEW.user_id, 'freemium', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '30 days', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER after_user_insert
            AFTER INSERT ON "users"
            FOR EACH ROW
            EXECUTE PROCEDURE create_freemium_subscription();
            """,
            reverse_sql="DROP TABLE subscription; DROP TYPE subscription_plan;"
        )
    ]
    
