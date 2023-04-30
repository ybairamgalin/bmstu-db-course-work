create table task_tracker.tokens(
    uuid text not null primary key,
    user_id bigint not null references task_tracker.users(id),
    expires_at timestamp not null
);
