from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    db)
from datetime import date
# Create your models here.

class Month(StructuredNode):
    value = IntegerProperty(unique_index=True, required=True)
    #day = RelationshipTo(Day, 'DAY')

class Year(StructuredNode):
    value = IntegerProperty(unique_index=True, required=True)
    month = RelationshipTo(Month, 'MONTH')

class NeoDate():
    day = IntegerProperty(index=True, required=True)
    '''
    def __init__(self, **args):

            year = args['year']
            month = args['month']
            self.day = args['day']

            year_lst = list(Year.nodes.filter(value=date.year))

            if year_lst:
                year = year_lst[0]
            else:
                year = Year(value=date.year).save()

            month_lst = year.month.match(value=date.month)
            
            if month_lst:
                month = month_lst[0] 
            else:
                month = Month(value=date.month).save()
                year.month.connect(month)

            day_lst = month.day.match(value=date.day)

            if day_lst:
                self.day = day_lst[0]
            else:
                self.day = Day(value=date.day).save()
                month.day.connect(self.day)
    '''
