from django.core.management.base import BaseCommand, CommandError
import subprocess
from members.models import create_adult
from members.models import create_child
from members.models import Child


class Command(BaseCommand):
    args = '<none>'
    help = 'Create pdf reports'

    def handle(self, *args, **options):
        inc = '\\documentclass [12pt, a4paper] {article}\n'
        inc += '\\usepackage{pdfpages}\n'
        inc += '\\begin{document}\n'
        for kid in Child.objects.all():
            tex_filename = 'reports/%s.tex' % kid.member.user.username
            pdf_filename = 'reports/%s.pdf' % kid.member.user.username
            file(tex_filename, 'w').write(kid.registrationFormLatex())
            subprocess.call('pdflatex -output-directory reports %s' % tex_filename, shell=True)

            inc += '\includepdf{' + pdf_filename + '}\n'
            file(tex_filename, 'w').write(kid.registrationFormLatex())
        inc += '\\end{document}\n'
        file('reports/all.tex', 'w').write(inc)
        subprocess.call('pdflatex -output-directory reports reports/all.tex', shell=True)
