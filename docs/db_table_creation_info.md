Project Tracker - SQL database setout with Creation queries.

These tables are to be created in this order, so the foreign keys dont 'break'.
(see the /docs folder for the Entity-Relationship diagrams)

1. account
    (no dependencies)
2. app_user 
    (depends on account)
3. project
    (depends on account, app_user)
4. task
    (depends on project, app_user)
5. project_access
    (depends on project, app_user)
6. materials_equipment
    (depends on project, app_user)
7. project_contacts
    (depends on project, app_user)
8. image
    (depends on app_user)
9. image_attachment
    (depends on image, app_user)
10. audit_log
    (depends on account, app_user)


 SQL queries to create these tables:
1. 
CREATE TABLE account (
    account_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL UNIQUE,
    account_email VARCHAR(320) NOT NULL UNIQUE
);

2. 
CREATE TABLE app_user (
	User_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	Account_id BIGINT NOT NULL,
	User_email VARCHAR(320) NOT NULL UNIQUE,
	Username VARCHAR(30) NOT NULL UNIQUE,
	Password CHAR(60) NOT NULL,
	First_name VARCHAR(50) NOT NULL,
	Last_name VARCHAR(50) NOT NULL,
	Last_login_time TIMESTAMPTZ,
	CONSTRAINT fk_user_owner
		FOREIGN KEY (account_id)
		REFERENCES account(account_id)
);

3.
CREATE TABLE project (
    project_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id BIGINT NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    address VARCHAR(320),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by BIGINT NOT NULL,
    CONSTRAINT fk_project_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES app_user(user_id),
    CONSTRAINT fk_project_owner
        FOREIGN KEY (account_id)
        REFERENCES account(account_id)
);
    
4. 
CREATE TABLE task (
    task_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id BIGINT NOT NULL,
    task_name VARCHAR(30) NOT NULL,
    task_description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by BIGINT NOT NULL,
    CONSTRAINT fk_task_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES app_user(user_id),
    CONSTRAINT fk_task_owner
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
);

5. 
CREATE TABLE project_access (
    project_id BIGINT PRIMARY KEY,
    access_details TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by BIGINT NOT NULL,
    CONSTRAINT fk_access_updated_by
        FOREIGN KEY (updated_by)
        REFERENCES app_user(user_id),
    CONSTRAINT fk_access_owner
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
);

6.
CREATE TABLE materials_equipment (
    project_id BIGINT PRIMARY KEY,
    materials_equipment_details TEXT,
    materials_equipment_updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    materials_equipment_updated_by BIGINT NOT NULL,
    CONSTRAINT fk_materials_equipment_updated_by
        FOREIGN KEY (materials_equipment_updated_by)
        REFERENCES app_user(user_id),
    CONSTRAINT fk_materials_equipment_owner
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
);

7.
CREATE TABLE project_contacts (
    project_id BIGINT PRIMARY KEY,
    project_contacts_notes TEXT,
    project_contacts_updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    project_contacts_updated_by BIGINT NOT NULL,
    CONSTRAINT fk_project_contacts_updated_by
        FOREIGN KEY (project_contacts_updated_by)
        REFERENCES app_user(user_id),
    CONSTRAINT fk_project_contacts_owner
        FOREIGN KEY (project_id)
        REFERENCES project(project_id)
);

8.
CREATE TABLE image (
    image_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_path TEXT NOT NULL,
    image_uploaded_by BIGINT NOT NULL,
    image_uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    entity_type VARCHAR(50) NOT NULL,
    CONSTRAINT fk_image_uploaded_by
        FOREIGN KEY (image_uploaded_by)
        REFERENCES app_user(user_id)
);

9.
CREATE TABLE image_attachment (
    image_attachment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NOT NULL,
    image_id BIGINT NOT NULL REFERENCES image(image_id),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by BIGINT NOT NULL REFERENCES app_user(user_id)
);

10.
CREATE TABLE audit_log (
    audit_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NOT NULL,
    account_id BIGINT NOT NULL REFERENCES account(account_id),
    performed_by BIGINT NOT NULL REFERENCES app_user(user_id),
    performed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    action VARCHAR(50) NOT NULL,
    details JSONB
);