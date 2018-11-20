drop table if exists student;
drop table if exists teacher;
drop table if exists project;
drop table if exists comments;

create table student(
  id integer PRIMARY KEY,
  email text unique not null,
  name text not null,
  dept text not null,
  session text not null,
  password text not null,
  current_course bit,
  project_id int
);

create table teacher(
  id integer primary key autoincrement,
  email text unique not null,
  name text not null,
  password text not null,
  dept text not null
);

create table project(
	id integer primary key autoincrement,
	course_code text not null,
	semester text not null,
	title text not null,
	description text not null,
  progress float check (progress <= 100),
  completed bit default 0,
  student_id int,
  teacher_id int,
  time timestamp default current_timestamp,
  foreign key (student_id) references student(id),
  foreign key (teacher_id) references teacher(id)
);

create table comments(
  id integer primary key autoincrement,
  project_id int,
  teacher_id int,
  time timestamp default current_timestamp,
  foreign key (project_id) references project(id),
  foreign key (teacher_id) references teacher(id)
);