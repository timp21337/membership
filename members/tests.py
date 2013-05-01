from django.test import TestCase
from members.models import *
from datetime import date
from django.contrib.auth.models import User


class MemberModelTest(TestCase):
    def test_creating_a_new_member_and_saving_it_to_the_database(self):

        initial_member_count = Member.objects.all().count()

        user = User.objects.create_user('bobp', 'bobp@paneris.org', 'password')
        user.first_name = "Bob"
        user.last_name = "Test"
        user.save()

        member = Member()
        member.user = user
        member.dob = date(2005, 07, 13)

        # check we can save it to the database
        member.save()

        # now check we can find it in the database again
        all_members_in_database = Member.objects.all()
        self.assertEquals(len(all_members_in_database), initial_member_count + 1)
        new_member_in_database = all_members_in_database[initial_member_count]
        self.assertEquals(new_member_in_database, member)

        self.assertEquals(new_member_in_database.user.first_name, "Bob")
        self.assertEquals(new_member_in_database.dob, member.dob)

        self.assertEquals('Bob (Test)', member.__unicode__())

        user.delete()

    def test_serialize_to_dict(self):
        c = self.create_test_child()
        print(dottedDict(c, 'child', {}))

    def test_render_to_tex(self):
        n = self.create_test_child_with_nulls()
        n_tex = n.registrationFormLatex()
        self.assertNotIn("Rahim", n_tex)
        c = self.create_test_child()
        c_tex = c.registrationFormLatex()
        self.assertIn("Rahim", c_tex)
#        self.assertEquals(n_tex, c_tex)
#        file('result.tex', 'w').write()
#        subprocess.call('pdflatex ./result.tex', shell=True)

    def create_test_child_with_nulls(self):
        tc = create_child('Tester', 'Test', 'F', '2004-08-22',
                          create_adult('Tim', 'Test', 'timp@example.org', 'M', '15 Campbell Road, Oxford, OX4 3NT',
                                       '01865 711036', '07768 894509'))
        tc.carer_2 = create_adult("Ruth", "Test", "Ruth@Test.net", "F", "", "", "07768894509")
        tc.emergency_contact = create_adult("Second", "Line", "second@example.org", "F", "", "", "07768 894509")
        tc.save()
        return tc

    def create_test_child(self):
        self.maxDiff = None
        tc = create_child('Jester', 'Jest', 'F', '2004-08-22',
                          create_adult('Jim', 'Test', 'timp@example.org', 'M', '15 Campbell Road, Oxford, OX4 3NT',
                                       '01865 711036', '07768 894509'))
        tc.carer_2 = create_adult("Ruth", "Jest", "Ruth@Test.net", "F", "", "", "07768894509")
        tc.emergency_contact = create_adult("Catch", "Line", "second@example.org", "F", "", "", "07768 894509")
        tc.doctor = create_adult("Dr", "Rahim", "", "M", "1 Manzil Way, Oxford OX4 3NT", "01865 77343", "")
        tc.allergies = "penicillin, pineapple"
        tc.save()
        return tc

    def create_child(self):
        c1 = create_adult('Primary', 'Carer', 'primary_carer@context-computing.co.uk', 'M', 'Home Address, Oxford, OX4 3NT', '01234', '07768343434')
        child = create_child('Child', 'One', 'F', '2004-10-27', c1)
        child.carer_2 = create_adult('Secondary', 'Carer', 'secondary_carer@context-computing.co.uk', 'F', 'Home Address, Oxford, OX4 3NT', '01234', '07768343435')
        child.doctor = create_doctor(create_adult('Dr', 'Test', '', 'F', 'The Surgery, Oxford', '01865 711333', '' ))
        child.backup = create_backup(create_adult('Backup', 'Contact', '', 'F', '', '', '07768 456788'))
        child.save()

    def test_output_command(self):
        self.create_child()
        Member.output()
        self.assert_file_exists('reports/all.pdf')

    def test_carers(self):
        self.create_child()
        self.assertEqual(['primary_carer', 'secondary_carer'], [m.user.username for m in Member.carers()])



    def assert_file_exists(self, file_path):
        "Assert a given file exists"
        self.assertTrue(os.path.exists(file_path), "%s does not exist!" % file_path)
