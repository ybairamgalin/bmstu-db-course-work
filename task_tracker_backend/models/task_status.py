from enum import Enum


class TaskStatus(str, Enum):
    open = 'Открыт'
    in_progress = 'В работе'
    blocked = 'Требуется информация'
    in_review = 'На ревью'
    closed = 'Закрыт'

    @staticmethod
    def map_db_status(db_status: str):
        if db_status == 'open':
            return TaskStatus.open
        if db_status == 'in_progress':
            return TaskStatus.in_progress
        if db_status == 'in_review':
            return TaskStatus.in_review
        if db_status == 'information_required':
            return TaskStatus.blocked
        if db_status == 'closed':
            return TaskStatus.closed

        raise RuntimeError('Map db status')

    def convert_to_db_status(self):
        if self == TaskStatus.open:
            return 'open'
        if self == TaskStatus.in_progress:
            return 'in_progress'
        if self == TaskStatus.in_review:
            return 'in_review'
        if self == TaskStatus.blocked:
            return 'information_required'
        if self == TaskStatus.closed:
            return 'closed'

        raise RuntimeError('Convert to db status')


