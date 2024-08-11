CREATE TABLE IF NOT EXISTS student (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL,
    name            TEXT NOT NULL,
    surname         TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS teacher (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL,
    password        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS timetable (
    id              TEXT PRIMARY KEY NOT NULL,
    name            TEXT NOT NULL,
    teacher_id      INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
);

CREATE TABLE IF NOT EXISTS class (
    id              SERIAL PRIMARY KEY,
    time            TIME NOT NULL,
    duration        INTEGER NOT NULL,
    index           INTEGER NOT NULL,
    day             INTEGER CHECK (day >= 0 AND day <= 6) NOT NULL,
    student_id      INTEGER,
    timetable_id    TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id),
    FOREIGN KEY (timetable_id) REFERENCES timetable (id)
);
