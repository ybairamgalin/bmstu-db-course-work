create table task_tracker.comments (
    id bigserial not null primary key,
    text text not null,
    task_id bigint not null references task_tracker.tasks(id),
    author_id bigint not null references task_tracker.users(id),
    created_at timestamp not null default now()
);

create index idx__comments__task_id on task_tracker.comments(task_id);
