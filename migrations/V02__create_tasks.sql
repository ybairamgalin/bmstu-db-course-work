create table if not exists task_tracker.users(
    id bigserial not null primary key,
    username text not null unique,
    name text,
    salt text not null,
    password text not null
);

create table if not exists task_tracker.tasks(
    id bigserial not null primary key,
    title text not null,
    content text,
    creator int8 not null,
    executor int8,
    public_id uuid unique default gen_random_uuid(),
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),

    foreign key (creator) references task_tracker.users(id),
    foreign key (executor) references task_tracker.users(id)
);
