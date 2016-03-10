from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom)
from datetime import date


class Day(StructuredNode):
    id = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    belongs = RelationshipFrom('Month', 'MONTH')


class Month(StructuredNode):
    id = StringProperty(unique_index=True)
    value = StringProperty(index=True)
    subset = RelationshipTo(Day, 'MONTH')
    belongs = RelationshipFrom('Year', 'YEAR')


class Year(StructuredNode):
    id = StringProperty(unique_index=True)
    subset = RelationshipTo(Month, 'YEAR')


class RootDate(StructuredNode):
    name = StringProperty(unique_index=True, default='root_date')
    subset = RelationshipTo(Year, 'DATE')


class NodeDate:

    def __init__(self, date):
        '''
        date is type date
        '''
        self.date = date

    @classmethod
    def to_date(self, datee):
        a = datee.id.split('-')
        return date(int(a[0]), int(a[1]), int(a[2]))

    def save(self):
        year = list(Year.nodes.filter(id=str(self.date.year)))
        if not year:
            year = Year(id=str(self.date.year)).save()
        else:
            year = year[0]

        month = list(
            Month.nodes.filter(
                id=str(self.date.year) + '-' + str(self.date.month)
                ))
        if not month:
            month = Month(
                id=str(self.date.year) + '-' + str(self.date.month),
                value=str(self.date.month)
            ).save()
        else:
            month = month[0]

        formatted_day = '{0}-{1}-{2}'.format(
                    self.date.year, self.date.month, self.date.day)
        day = list(Day.nodes.filter(id=formatted_day))
        if not day:
            day = Day(id=formatted_day, value=str(self.date.day)).save()
        else:
            day = day[0]

        root = list(RootDate.nodes.all())
        if not root:
            raise EnvironmentError('Execute ./manage.py setup_date_environ')
        root[0].subset.connect(year)
        year.subset.connect(month)
        month.subset.connect(day)
        return day
