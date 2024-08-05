CREATE TABLE IF NOT EXISTS student (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL,
    name            TEXT NOT NULL,
    surname         TEXT NOT NULL,
    classes         INTEGER[]
);

CREATE TABLE IF NOT EXISTS teacher (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS class (
    id              SERIAL PRIMARY KEY,
    time            TIME NOT NULL,
    duration        INTEGER NOT NULL,
    day             INTEGER CHECK (day >= 1 AND day <= 7) NOT NULL,
    student_id      INTEGER,
    teacher_id      INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
);

CREATE TABLE IF NOT EXISTS timetable (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    teacher_id      INTEGER NOT NULL,
    classes         INTEGER[],
    days_of_week    INTEGER[],
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
);
