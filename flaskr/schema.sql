CREATE TABLE IF NOT EXISTS student (
    id              SERIAL PRIMARY KEY,
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
    day             INTEGER CHECK (day >= 1 AND day <= 7),
    student_id      INTEGER,
    FOREIGN KEY (student_id) REFERENCES student (id)
);

CREATE TABLE IF NOT EXISTS timetable (
    id              SERIAL PRIMARY KEY,
    teacher_id      INTEGER NOT NULL,
    classes         INTEGER[],
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
);
