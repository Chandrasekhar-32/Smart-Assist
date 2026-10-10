-- SmartAssist database schema (PostgreSQL dialect, spec section 21)
-- Generated from the SQLAlchemy models in backend/app/models/
-- SQLite users: tables are created automatically by backend/app/seed.py

CREATE TABLE subjects (
	id SERIAL NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE users (
	id SERIAL NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE lessons (
	id SERIAL NOT NULL, 
	subject_id INTEGER NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	description TEXT, 
	difficulty VARCHAR(20) NOT NULL, 
	position INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_id) REFERENCES subjects (id)
);

CREATE TABLE student_profiles (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	age INTEGER, 
	preferred_format VARCHAR(30) NOT NULL, 
	learning_requirement VARCHAR(30), 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE quizzes (
	id SERIAL NOT NULL, 
	lesson_id INTEGER NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (lesson_id), 
	FOREIGN KEY(lesson_id) REFERENCES lessons (id)
);

CREATE TABLE resources (
	id SERIAL NOT NULL, 
	lesson_id INTEGER NOT NULL, 
	type VARCHAR(30) NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	content TEXT, 
	media_url VARCHAR(400), 
	PRIMARY KEY (id), 
	FOREIGN KEY(lesson_id) REFERENCES lessons (id)
);

CREATE TABLE student_progress (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	lesson_id INTEGER NOT NULL, 
	progress_percentage FLOAT NOT NULL, 
	completed BOOLEAN NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES users (id), 
	FOREIGN KEY(lesson_id) REFERENCES lessons (id)
);

CREATE TABLE attempts (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	quiz_id INTEGER NOT NULL, 
	score INTEGER NOT NULL, 
	percentage FLOAT NOT NULL, 
	time_taken INTEGER NOT NULL, 
	attempt_number INTEGER NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES users (id), 
	FOREIGN KEY(quiz_id) REFERENCES quizzes (id)
);

CREATE TABLE questions (
	id SERIAL NOT NULL, 
	quiz_id INTEGER NOT NULL, 
	question TEXT NOT NULL, 
	option_a TEXT NOT NULL, 
	option_b TEXT NOT NULL, 
	option_c TEXT NOT NULL, 
	option_d TEXT NOT NULL, 
	correct_answer VARCHAR(1) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quiz_id) REFERENCES quizzes (id)
);

CREATE TABLE recommendations (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	lesson_id INTEGER, 
	resource_id INTEGER, 
	recommended_format VARCHAR(30) NOT NULL, 
	difficulty VARCHAR(20) NOT NULL, 
	confidence FLOAT NOT NULL, 
	reason TEXT NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES users (id), 
	FOREIGN KEY(lesson_id) REFERENCES lessons (id), 
	FOREIGN KEY(resource_id) REFERENCES resources (id)
);
