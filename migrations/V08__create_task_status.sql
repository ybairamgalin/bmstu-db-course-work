create type task_tracker.task_status as enum (
    'open',
    'in_progress',
    'in_review',
    'information_required',
    'closed'
);

alter table task_tracker.tasks
    add column status task_tracker.task_status default 'open';
