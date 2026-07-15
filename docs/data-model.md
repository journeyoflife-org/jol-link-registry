# Data Model

## Entities

### Category

| Field       | Type         | Constraints        |
| ----------- | ------------ | ------------------ |
| id          | UUID         | PK                 |
| name        | VARCHAR(255) | UNIQUE, NOT NULL   |
| slug        | VARCHAR(255) | UNIQUE, NOT NULL   |
| description | TEXT         | nullable           |
| created_at  | TIMESTAMPTZ  | server default now |

### Link

| Field           | Type          | Constraints        |
| --------------- | ------------- | ------------------ |
| id              | UUID          | PK                 |
| url             | VARCHAR(2048) | NOT NULL           |
| title           | VARCHAR(512)  | NOT NULL           |
| description     | TEXT          | nullable           |
| country_code    | VARCHAR(2)    | NOT NULL           |
| is_active       | BOOLEAN       | default true       |
| last_checked_at | TIMESTAMPTZ   | nullable           |
| created_at      | TIMESTAMPTZ   | server default now |
| updated_at      | TIMESTAMPTZ   | auto-update        |
| category_id     | UUID          | FK → categories.id |

## Relationships

- A Category has many Links (one-to-many).
