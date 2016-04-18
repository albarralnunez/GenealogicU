from django.db import IntegrityError


def check_date_after_birth(event, person):
    # birth restriction
    birth = person.son.all()
    if birth:
        date_begin_birth = None
        date_begin_event = None
        # check birth date
        date_beg = birth[0].date_begin.all()
        if date_beg:
            date_begin_birth = date_beg[0]
        # chekc event dates
        date_beg = event.date_begin.all()
        if date_beg:
            date_begin_event = date_beg[0]
        # check restriction
        if date_begin_event and date_begin_birth:
            if date_begin_event.ordinal <= date_begin_birth.ordinal:
                raise IntegrityError('date_begin of this event must be greater than date_begin of birth event of this person')


def check_date_befor_death(event, person):
    # death restriction
    death = person.death.all()
    if death:
        date_end_death = None
        date_end_event = None
        # check death date
        date_en = death[0].date_end.all()
        if date_en:
            date_end_death = date_en[0]
        # chekc event dates
        date_en = event.date_end.all()
        if date_en:
            date_end_event = date_en[0]
        # check restriction
        if date_end_event and date_end_death:
            if date_end_event.ordinal >= date_end_death.ordinal:
                raise IntegrityError('date_end of this event must be lower than date_end of death event of this person')


def check_begin_end(date_begin, date_end):
    if date_begin and date_end:
        if date_begin > date_end:
            raise IntegrityError('date_begin must be lower than date_end')
