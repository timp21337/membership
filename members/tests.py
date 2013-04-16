from django.test import TestCase
from members.models import Member
from datetime import date


class MemberModelTest(TestCase):
    def test_creating_a_new_member_and_saving_it_to_the_database(self):
        # start by creating a new member object with its "question" set
        member = Member()
        member.first_name = "Bob"
        member.dob = date(2005, 07, 13)

        # check we can save it to the database
        member.save()

        # now check we can find it in the database again
        all_members_in_database = Member.objects.all()
        self.assertEquals(len(all_members_in_database), 1)
        only_member_in_database = all_members_in_database[0]
        self.assertEquals(only_member_in_database, member)

        # and check that it's saved its two attributes: question and pub_date
        self.assertEquals(only_member_in_database.first_name, "Bob")
        self.assertEquals(only_member_in_database.dob, member.dob)

