from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        dir=os.path.dirname(os.path.abspath(__file__))+'/../../../media'
        try:
            for i in os.listdir(dir):
                subdir=os.listdir(os.path.join(dir,i))
                for j in subdir:
                    os.remove(os.path.join(dir+'/'+i,j))
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
            return
        self.stdout.write(self.style.SUCCESS('Images removed succesfully'))