import geneTree.models_person as models
from .gedcom_parser import Gedcom
# from .tasks import check_coincidence
from neomodel import db
from datetime import datetime


class GedcomUploader:

    def __init__(self, gedcom_file):
        '''
        __persons = {element pointer: Person}
        '''
        self.data = Gedcom(gedcom_file)
        self.__persons = {}

    def __create_persons(self):
        for iden in self.data.element_dict():
            act_ele = self.data.element_dict()[iden]
            if act_ele.is_individual():
                name, surname = act_ele.name()
                gender = act_ele.gender()
                act_p = models.Person(
                    name=name if name else None,
                    surname=surname if surname else None,
                    genere=gender if gender else None
                    ).save()
                self.__persons[act_ele.pointer()] = act_p
                act_p.tree.connect(self.tree)

    def __marriage(self, act_ele):
        spouses = self.data.get_family_members(act_ele, "PARENTS")
        spouses_obj = [self.__persons[x.pointer()] for x in spouses]
        if len(spouses_obj) > 1:
            date, place = self.data.marriage(spouses[0], spouses[1])
            if date:
                date = date.split(' ')
                date = ' '.join(
                    [date[0], date[1][0] + date[1][1:].lower(), date[2]])
                date = datetime.strptime(
                        date, "%d %b %Y")
            m = models.Marriage().save()
            m.add_spouse(spouses_obj[0])
            m.add_spouse(spouses_obj[1])
            m.set_event(location_prop=place, date_begin=date, date_end=date)
        return spouses_obj

    def __childs(self, act_ele, spouses):
        childs = self.data.get_family_members(act_ele, "CHIL")
        childs_obj = [self.__persons[x.pointer()] for x in childs]
        b = None
        for child in childs_obj:
            b = models.Birth().save()
            b.set_son(child)
            for spouse in spouses:
                b.add_father(spouse)
        return childs_obj

    def __create_relations(self):
        for iden in self.data.element_dict():
            act_ele = self.data.element_dict()[iden]
            if act_ele.is_family():
                #  marriages
                spouses = self.__marriage(act_ele)

                #  childs
                self.__childs(act_ele, spouses)

                #  marriages test
                print 'Family:'
                print '  $spouses$'
                fam = self.data.get_family_members(act_ele, "PARENTS")
                #  if len(fam) > 1:
                #       print self.data.marriage(fam[0], fam[1])
                for spouse in fam:
                    print '-------------------------------'
                    print '  ' + str(spouse.name())
                    print '  ' + str(spouse.pointer())
                    print '  ' + str(spouse.tag())
                    print '-------------------------------'

                # childs test
                print '    $childs$'
                for child in self.data.get_family_members(act_ele, "CHIL"):
                    print '-------------------------------'
                    print '    ' + str(child.name())
                    print '    ' + str(child.pointer())
                    print '-------------------------------'

    # def ___analize(self):
    #     for p in self.__persons:
    #         p.check_coincidences()

    @db.transaction
    def upload(self, tree):
        self.tree = tree
        #  all persons
        print 'Create persons'
        self.__create_persons()
        #  all families
        print 'Create relations'
        self.__create_relations()
        # self.__analize()
        print 'upload finished'
