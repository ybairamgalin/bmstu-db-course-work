create table task_tracker.tags(
    id bigserial not null primary key,
    value text not null unique
);

create table task_tracker.task_tags(
    task_id bigint not null references task_tracker.tasks,
    tag_id bigint not null references task_tracker.tags,
    primary key (task_id, tag_id)
);
