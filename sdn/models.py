from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Controller(models.Model):
    name = models.CharField(max_length=200)
    ip_addr = models.CharField(max_length=15)
    port = models.CharField(max_length=4)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class ControllerType(models.TextChoices):
        EMPOWER = 'EM', _('Empower')

    controller_type = models.CharField(
        max_length=2,
        choices=ControllerType.choices,
        default=ControllerType.EMPOWER
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sdn:controller-view', args=[])


class Tenant(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    long_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sdn:tenant-view', args=[])

    def get_association_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.ASSOCIATION).order_by('name')

    def get_int_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.INT).order_by('name')

    def get_throughput_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.THROUGHPUT).order_by('name')

    def get_mcda_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.MCDA).order_by('name')

    def get_delay_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.DELAY).order_by('name')

    def get_other_graphs(self):
        return self.controller.graph_set.filter(graph_type=Graph.GraphType.OTHER).order_by('name')


class Graph(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    iframe_url = models.CharField(max_length=200)

    class GraphType(models.TextChoices):
        THROUGHPUT = 'TH', _('Throughput')
        DELAY = 'DE', _('Delay')
        INT = 'IN', _('In-band Network Telemetry')
        ASSOCIATION = 'AS', _('Association Status')
        MCDA = 'MC', _('MCDA')
        OTHER = 'OT', _('Other')

    graph_type = models.CharField(
        max_length=2,
        choices=GraphType.choices,
        default=GraphType.OTHER,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['graph_type', 'name']

    def get_absolute_url(self):
        return reverse('sdn:graph-view', args=[])
