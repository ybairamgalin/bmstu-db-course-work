create table task_tracker.topics(
    id bigserial not null primary key,
    name text not null unique
);

alter table task_tracker.tasks add column
    topic_id bigint references task_tracker.topics(id);
