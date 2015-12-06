from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom)
from datetime import datetime
from django.core.exceptions import ValidationError


class Day(StructuredNode):
    id = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    belongs = RelationshipFrom('Month', 'SUBSET')


class Month(StructuredNode):
    id = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    subset = RelationshipTo(Day, 'SUBSET')
    belongs = RelationshipFrom('Year', 'SUBSET')


class Year(StructuredNode):
    id = StringProperty(unique_index=True)
    subset = RelationshipTo(Month, 'SUBSET')


class RootDate(StructuredNode):
    subset = RelationshipTo(Year, 'DATE')


class NodeDate:

    def __init__(self, date):

        date = date.split('-')
        if len(date[2]) < 2:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")
        elif len(date[1]) < 2:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")
        elif len(date[0]) < 4:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")

        a_month = 1 if date[1] == '00' else int(date[1])
        a_day = 1 if not date[2] == '00' else int(date[2])
        a_year = int(date[0])
        validator = '{y}-{m}-{d}'.format(y=a_year, m=a_month, d=a_day)
        try:
            datetime.strptime(validator, '%Y-%m-%d')
        except ValidationError:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")
        self.year = a_year
        self.month = a_month
        self.day = a_day

    def save(self):

        year = list(Year.nodes.filter(id=str(self.year)))
        if not year:
            year = Year(id=str(self.year)).save()
        else:
            year = year[0]

        month = list(
            Month.nodes.filter(
                id=str(self.year) + '-' + str(self.month)
                ))
        if not month:
            month = Month(
                id=str(self.year) + '-' + str(self.month),
                value=str(self.month)
            ).save()
        else:
            month = month[0]

        formatted_day = '{0}-{1}-{2}'.format(
                    self.year, self.month, self.day)
        day = list(Day.nodes.filter(id=formatted_day))
        if not day:
            day = Day(id=formatted_day, value=str(self.day)).save()
        else:
            day = day[0]

        root = list(RootDate.nodes.all())
        if not root:
            raise EnvironmentError('Execute ./manage.py setup_date_environ')
        root[0].subset.connect(year)
        year.subset.connect(month)
        month.subset.connect(day)

        return day
