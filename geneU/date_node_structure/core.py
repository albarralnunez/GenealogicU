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

    def __init__(self, year, month=0, day=0):
        a_moth = 1 if not month else month
        a_day = 1 if not day else day
        validator = '{0}-{1}-{2}'.format(year, a_moth, a_day)
        try:
            datetime.strptime(validator, '%Y-%m-%d')
        except ValidationError:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")
        self.year = year
        self.month = month
        self.day = day

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
