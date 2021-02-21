CREATE TABLE IF NOT EXISTS "person" (
	id SERIAL PRIMARY KEY,
	first_name TEXT,
	last_name TEXT,
	email TEXT,
	address TEXT,
	skills TEXT[]
	);
CREATE TABLE IF NOT EXISTS "project" (
    id SERIAL PRIMARY KEY,
    project_name TEXT,
    date_posted TEXT,
    department TEXT,
    description TEXT,
    skills TEXT[]
)