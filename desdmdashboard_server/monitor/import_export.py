
import tarfile
import StringIO

from django.db.models import get_app, get_models
from django.core import serializers


def write_tar_dump_for_app(appname, dataformat='json'):

    app = get_app(appname)
    models = get_models(app)

    tar = tarfile.open(appname+'_dump.tar', 'w')

    for model in models:
        modelname = model.__name__
        jsons = serializers.serialize(dataformat, model.objects.all())

        string = StringIO.StringIO()
        string.write(jsons)
        string.seek(0)
        info = tarfile.TarInfo(name=modelname)
        info.size = len(string.buf)

        tar.addfile(tarinfo=info, fileobj=string)

    tar.close()


def load_json_tar_dump_into_db(filename, dataformat='json', update_only=True):
    tar = tarfile.open(filename, 'r')

    for member in tar.getmembers():
        fi = tar.extractfile(member)
        datastr = fi.read()

        for desmet in serializers.deserialize(dataformat, datastr):

            if update_only:
                model = type(desmet.object)
                if model.objects.filter(pk=desmet.object.pk):
                    continue
                else:
                    desmet.save()
            else:
                desmet.save()
