from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    # For schedule
    schedule_subject = State()
    schedule_day = State()
    schedule_time = State()
    schedule_room = State()

    # For deadlines
    deadline_subject = State()
    deadline_task = State()
    deadline_link = State()
    deadline_due = State()

    # For exams
    exam_subject = State()
    exam_type = State()  # midterm or final
    exam_datetime = State()
    exam_room = State()