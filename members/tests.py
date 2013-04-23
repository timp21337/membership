from django.test import TestCase
from members.models import Member
from datetime import date
from django.contrib.auth.models import User


class MemberModelTest(TestCase):
    def test_creating_a_new_member_and_saving_it_to_the_database(self):

        user = User.objects.create_user('bobp', 'bobp@paneris.org', 'password')
        user.first_name = "Bob"
        user.last_name = "Pizey"
        user.save()

        member = Member()
        member.user = user

        member.dob = date(2005, 07, 13)

        # check we can save it to the database
        member.save()

        # now check we can find it in the database again
        all_members_in_database = Member.objects.all()
        self.assertEquals(len(all_members_in_database), 1)
        only_member_in_database = all_members_in_database[0]
        self.assertEquals(only_member_in_database, member)

        self.assertEquals(only_member_in_database.user.first_name, "Bob")
        self.assertEquals(only_member_in_database.dob, member.dob)

        self.assertEquals('Bob (Pizey)', member.__unicode__())

        user.delete()