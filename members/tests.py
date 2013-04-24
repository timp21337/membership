from django.test import TestCase
from members.models import Member
from members.models import Child
from datetime import date
from django.contrib.auth.models import User


class MemberModelTest(TestCase):
    def test_creating_a_new_member_and_saving_it_to_the_database(self):

        initial_member_count = Member.objects.all().count()
        initial_child_count = Child.objects.all().count()

        user = User.objects.create_user('bobp', 'bobp@paneris.org', 'password')
        user.first_name = "Bob"
        user.last_name = "Pizey"
        user.save()

        member = Member()
        member.user = user

        # check we can save it to the database
        member.save()

        child = Child()
        child.member = member
        child.dob = date(2005, 07, 13)
        child.save()

        # now check we can find it in the database again
        all_members_in_database = Member.objects.all()
        self.assertEquals(len(all_members_in_database), initial_member_count + 1)
        new_member_in_database = all_members_in_database[initial_member_count]
        self.assertEquals(new_member_in_database, member)

        self.assertEquals(new_member_in_database.user.first_name, "Bob")

        all_children_in_database = Child.objects.all()
        self.assertEquals(len(all_children_in_database), initial_child_count + 1)
        new_child_in_database = all_children_in_database[initial_child_count]

        self.assertEquals(new_child_in_database.dob, child.dob)

        self.assertEquals('Bob (Pizey)', member.__unicode__())
        self.assertEquals('Bob (Pizey)', child.__unicode__())



        user.delete()

