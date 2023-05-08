create table task_tracker.timers(
    id bigserial not null primary key,
    started_at timestamp not null default now(),
    stopped_at timestamp,
    task_id bigint references task_tracker.tasks,
    started_by bigint references task_tracker.users
);

create index idx__timers__task_id on task_tracker.timers(task_id);
create index idx__timers__task_id__stopped_at on task_tracker.timers(task_id, stopped_at);

alter table task_tracker.tasks add column spent_time interval default null;
