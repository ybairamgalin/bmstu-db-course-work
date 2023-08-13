create table task_tracker.timers(
    id bigserial not null primary key,
    started_at timestamp not null default now(),
    stopped_at timestamp default null,
    task_id bigint not null references task_tracker.tasks,
    started_by bigint not null references task_tracker.users,

    -- so that only one active timer was allowed
    unique(task_id, stopped_at)
);

alter table task_tracker.tasks add column spent_time interval default null;
