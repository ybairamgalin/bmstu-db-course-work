begin transaction;

delete from task_tracker.tasks;
delete from task_tracker.users;

insert into task_tracker.users(id, username, name, salt, password)
values
    (1, 'ybairamgalin', 'Yaroslav Bairamgalin', 'aslfhe', 'password'),
    (2, 'bayyar', 'Valera Ivanov', 'aslfhe', 'password'),
    (3, 'ipetrov', 'Ivan Petrov', 'aslfhe', 'password');

insert into task_tracker.tasks(id, title, content, creator, executor, created_at, updated_at)
values
    (1, 'Сделать крсовую работу', 'До мая', '1', '2', '2022-01-14 12:34:13', '2022-01-14 19:46:13'),
    (2, 'Закрыть ФИЛП', 'ляля', '2', '2', '2022-03-14 12:34:13', '2022-10-14 12:44:13'),
    (3, 'task title 3', 'task content 3', '1', '1', '2022-03-03 12:34:13', '2022-10-03 12:44:13'),
    (4, 'task title 4', 'task content 4', '2', '2', '2022-03-04 12:34:13', '2022-10-04 12:44:13'),
    (5, 'task title 5', 'task content 5', '3', '3', '2022-03-05 12:34:13', '2022-10-05 12:44:13'),
    (6, 'task title 6', 'task content 6', '1', '2', '2022-03-06 12:34:13', '2022-10-06 12:44:13'),
    (7, 'task title 7', 'task content 7', '2', '1', '2022-03-07 12:34:13', '2022-10-07 12:44:13'),
    (8, 'task title 8', 'task content 8', '3', '3', '2022-03-08 12:34:13', '2022-10-08 12:44:13'),
    (9, 'task title 9', 'task content 9', '1', '1', '2022-03-09 12:34:13', '2022-10-09 12:44:13'),
    (10, 'task title 10', 'task content 10', '2', '3', '2022-10-03 12:34:13', '2022-10-10 12:44:13'),
    (11, 'task title 11', 'task content 11', '3', '1', '2022-11-03 12:34:13', '2022-10-11 12:44:13');

commit transaction;
