import json
from django.shortcuts import render
from django.http import HttpResponse

from mstdnmap.mstdn.models import Instance


def index(request):

    return render(request, "index.html")


def map_json(request):

    instances = Instance.objects.all().prefetch_related("connections")
    connections = set()

    for instance in instances:
        from_id = instance.id
        for target in instance.connections.all():
            to_id = target.id
            print(to_id, to_id)
            connections.add((min(from_id, to_id), max(from_id, to_id)))

    data = {
        "instances": [
            {"id": i.id, "hostname": i.hostname}
            for i in instances
        ],
        "connections": list(connections)
    }
    return HttpResponse(json.dumps(data, indent=2), content_type="application/json")
