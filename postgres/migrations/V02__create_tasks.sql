create table if not exists task_tracker.users(
    id int8 not null generated always as identity primary key,
    username text not null unique,
    name text,
    salt text not null,
    password text not null
);

create table if not exists task_tracker.tasks(
    id int8 not null generated always as identity primary key,
    title text not null,
    content text,
    creator int8 not null,
    executor int8,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),

    foreign key (creator) references task_tracker.users(id),
    foreign key (executor) references task_tracker.users(id)
);
