from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Tenant, Controller, Graph
from .forms import TenantForm, ControllerForm, GraphForm

import requests


class IndexView(generic.ListView):
    template_name = 'sdn/index.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        """
        Return all tenants.
        """
        return Tenant.objects.all()


class TenantView(generic.ListView):
    template_name = 'sdn/tenants.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        """
        Return all tenants.
        """
        return Tenant.objects.all()


class ControllerView(generic.ListView):
    template_name = 'sdn/controllers.html'
    context_object_name = 'controllers'

    def get_queryset(self):
        """
        Return all controllers.
        """
        return Controller.objects.all()


class GraphView(generic.ListView):
    template_name = 'sdn/graphs.html'
    context_object_name = 'graphs'

    def get_queryset(self):
        """
        Return all graphs.
        """
        return Graph.objects.all()


class TenantCreate(SuccessMessageMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name_suffix = '-form'
    success_message = "Tenant %(name)s was created successfully!"


class ControllerCreate(SuccessMessageMixin, CreateView):
    model = Controller
    form_class = ControllerForm
    template_name_suffix = '-form'
    success_message = "Controller %(name)s was created successfully!"


class GraphCreate(SuccessMessageMixin, CreateView):
    model = Graph
    form_class = GraphForm
    template_name_suffix = '-form'
    success_message = "Graph %(name)s was created successfully!"


class TenantUpdate(SuccessMessageMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name_suffix = '-form'
    success_message = "Tenant %(name)s was updated successfully!"


class ControllerUpdate(SuccessMessageMixin, UpdateView):
    model = Controller
    form_class = ControllerForm
    template_name_suffix = '-form'
    success_message = "Controller %(name)s was updated successfully!"


class GraphUpdate(SuccessMessageMixin, UpdateView):
    model = Graph
    form_class = GraphForm
    template_name_suffix = '-form'
    success_message = "Graph %(name)s was updated successfully!"


class TenantDelete(DeleteView):
    model = Tenant
    success_url = reverse_lazy('sdn:tenant-view')
    success_message = "Tenant %(name)s was deleted successfully!"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return self.delete(request, *args, **kwargs)


class ControllerDelete(DeleteView):
    model = Controller
    success_url = reverse_lazy('sdn:controller-view')
    success_message = "Controller %(name)s was deleted successfully!"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return self.delete(request, *args, **kwargs)


class GraphDelete(DeleteView):
    model = Graph
    success_url = reverse_lazy('sdn:graph-view')
    success_message = "Graph %(name)s was deleted successfully!"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return self.delete(request, *args, **kwargs)


class TenantSelectView(generic.ListView):
    template_name = 'sdn/tenant-select.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        """
        Return all tenants.
        """
        return Tenant.objects.all()


def parse_traffic_rules_from_empower(json_obj, tenant_id):
    traffic_rules = []
    crr_id = 1
    for t in json_obj:
        if 'tenant_id' in t:
            if tenant_id == t['tenant_id'] and 'traffic_rules' in t:
                for tr in t['traffic_rules']:
                    crr_tr = {
                        'id': crr_id,
                        'label': t['traffic_rules'][tr]['label'],
                        'dscp': t['traffic_rules'][tr]['dscp'],
                        'match': t['traffic_rules'][tr]['match'],
                        'priority': t['traffic_rules'][tr]['priority']
                    }
                    crr_id += 1
                    traffic_rules.append(crr_tr)
        return traffic_rules


def parse_slices_from_empower(json_obj, tenant_id):
    slices = []
    crr_id = 1
    for t in json_obj:
        if 'tenant_id' in t:
            if tenant_id == t['tenant_id'] and 'slices' in t:
                for dscp in t['slices']:
                    crr_slc = {
                        'id': crr_id,
                        'wtp': 'All',
                        'dscp': dscp,
                        'amsdu': t['slices'][dscp]['wifi']['static-properties']['amsdu_aggregation'],
                        'quantum': t['slices'][dscp]['wifi']['static-properties']['quantum'],
                        'scheduler': t['slices'][dscp]['wifi']['static-properties']['scheduler']
                    }
                    crr_id += 1
                    slices.append(crr_slc)
                    for wtp in t['slices'][dscp]['wifi']['wtps']:
                        crr_slc = {
                            'id': crr_id,
                            'wtp': wtp,
                            'dscp': dscp
                        }
                        if 'amsdu_aggregation' in t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']:
                            crr_slc['amsdu'] = t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']['amsdu_aggregation']
                        else:
                            crr_slc['amsdu'] = t['slices'][dscp]['wifi']['static-properties']['amsdu_aggregation']

                        if 'quantum' in t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']:
                            crr_slc['quantum'] = t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']['quantum']
                        else:
                            crr_slc['quantum'] = t['slices'][dscp]['wifi']['static-properties']['quantum']

                        if 'scheduler' in t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']:
                            crr_slc['scheduler'] = t['slices'][dscp]['wifi']['wtps'][wtp]['static-properties']['scheduler']
                        else:
                            crr_slc['scheduler'] = t['slices'][dscp]['wifi']['static-properties']['scheduler']



                        crr_id += 1
                        slices.append(crr_slc)
        return slices


def parse_apps_from_empower(json_obj, tenant_id):
    apps = []
    for t in json_obj:
        if 'tenant_id' in t:
            if tenant_id == t['tenant_id'] and 'empower.apps.btw.handlers.appbrokerhandler' in t['components']:
                for app_id in t['components']['empower.apps.btw.handlers.appbrokerhandler']['apps']:
                    crr_app = t['components']['empower.apps.btw.handlers.appbrokerhandler']['apps'][app_id]
                    app_info = {
                        'id': app_id,
                        'jitter_ms': crr_app['app-ctrl:cc']['app-req'][1]['jitter_ms'],
                        'rtt_ms': crr_app['app-ctrl:cc']['app-req'][1]['rtt_ms']
                    }
                    apps.append(app_info)
        return apps


def parse_topology_from_empower(json_obj, tenant_id):
    topology = {'nodes': [], 'edges': [], 'wtps': [], 'lvaps': []}
    shape = 'dot'
    for t in json_obj:
        if 'tenant_id' in t:
            if tenant_id == t['tenant_id'] and 'lvaps' in t and 'wtps' in t:
                lvaps = t['lvaps']
                wtps = t['wtps']
                for wtp in wtps:
                    wtp_color = '#FB7E81'
                    if 'state' in wtps[wtp]:
                        if wtps[wtp]['state'] == 'online':
                            wtp_color = '#97C2FC'
                    wtp_label = wtp
                    topology['nodes'].append({'id': wtp, 'label': wtp_label, 'shape': shape, 'color': wtp_color})
                    topology['wtps'].append({'addr': wtp, 'label': wtp_label})

                lvap_color = '#000000'
                for lvap in lvaps:
                    topology['nodes'].append({'id': lvap, 'label': lvap, 'shape': shape, 'color': lvap_color})
                    topology['lvaps'].append({'addr': lvap, 'label': lvap})
                    if 'blocks' in lvaps[lvap]:
                        if lvaps[lvap]['blocks']:
                            # if lvaps[lvap]['blocks'][0] is not None:
                            if 'addr' in lvaps[lvap]['blocks'][0]:
                                connected_wtp = lvaps[lvap]['blocks'][0]['addr']
                                topology['edges'].append({'from': lvap,
                                                          'to': connected_wtp,
                                                          'color': {'color': 'black'},
                                                          'dashes': 'true'})
            # Creating wired links
            for i in range(0, len(topology['wtps'])-1):
                topology['edges'].append({'from': topology['wtps'][i]['addr'],
                                          'to': topology['wtps'][i+1]['addr']})
        return topology


class DataPlaneView(generic.DetailView):
    model = Tenant
    template_name = 'sdn/tenant-visualization.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['tenants'] = Tenant.objects.all()
        return context


def send_slice_config(request, tenant_id):
    if request.POST:
        tenant = get_object_or_404(Tenant, pk=tenant_id)

        if tenant.controller.controller_type == Controller.ControllerType.EMPOWER:
            wtp = request.POST['wtp']
            dscp = request.POST['dscp']
            quantum = request.POST['quantum']
            amsdu = request.POST['amsdu']
            scheduler = request.POST['scheduler']
            url = 'http://' + tenant.controller.ip_addr + ':' + tenant.controller.port + '/api/v1/tenants/' + \
                  tenant.long_id + '/components/empower.apps.managers.slicemanager'
            payload = {
                'version': '1.0',
                'params': {
                    'dscp': dscp,
                    'quantum': int(quantum),
                    'amsdu': amsdu,
                    'scheduler': int(scheduler),
                    "config_slice": True
                }
            }
            if wtp != 'all':
                payload['params']['wtp_addr'] = str(wtp)
            try:
                r = requests.put(url, json=payload, auth=(tenant.controller.user, tenant.controller.password))
                if r.status_code != 204:
                    response = JsonResponse({"error": "Configuration not sent to the controller!"})
                    response.status_code = r.status_code
                    return response
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
    return HttpResponse('')


def send_mcda_config(request, tenant_id):
    if request.POST:
        tenant = get_object_or_404(Tenant, pk=tenant_id)

        if tenant.controller.controller_type == Controller.ControllerType.EMPOWER:
            active = request.POST['active']
            app = request.POST['app']
            qos_channel_load_rate = request.POST['qos_channel_load_rate']
            qos_rssi = request.POST['qos_rssi']
            qos_expected_load = request.POST['qos_expected_load']
            qos_measured_load = request.POST['qos_measured_load']
            qos_queueing_delay = request.POST['qos_queueing_delay']
            qos_association_status = request.POST['qos_association_status']
            be_channel_load_rate = request.POST['be_channel_load_rate']
            be_rssi = request.POST['be_rssi']
            be_expected_load = request.POST['be_expected_load']
            be_measured_load = request.POST['be_measured_load']
            be_queueing_delay = request.POST['be_queueing_delay']
            be_association_status = request.POST['be_association_status']
            url = 'http://' + tenant.controller.ip_addr + ':' + tenant.controller.port + '/api/v1/tenants/' + \
                  tenant.long_id + '/components/' + app

            payload = {
                'version': '1.0',
                'params': {
                    "active": False
                }
            }

            if active == 'true':
                payload['params']['active'] = True
                payload['params']['mcda_descriptor'] = {}
                payload['params']['mcda_descriptor']['criteria'] = [
                    "wtp_channel_load_rate",
                    "wtp_sta_rssi_dbm",
                    "wtp_load_expected_mbps",
                    "wtp_load_measured_mbps",
                    "wtp_queue_delay_ms",
                    "sta_association_flag"
                ]
                payload['params']['mcda_descriptor']['targets'] = [
                    "MIN",
                    "MAX",
                    "MIN",
                    "MIN",
                    "MIN",
                    "MAX"
                ]
                payload['params']['mcda_descriptor']['weights_qos'] = [
                    qos_channel_load_rate,
                    qos_rssi,
                    qos_expected_load,
                    qos_measured_load,
                    qos_queueing_delay,
                    qos_association_status
                ]
                payload['params']['mcda_descriptor']['weights_be'] = [
                    be_channel_load_rate,
                    be_rssi,
                    be_expected_load,
                    be_measured_load,
                    be_queueing_delay,
                    be_association_status
                ]
            try:
                r = requests.put(url, json=payload, auth=(tenant.controller.user, tenant.controller.password))
                if r.status_code != 204:
                    response = JsonResponse({"error": "Configuration not sent to the controller!"})
                    response.status_code = r.status_code
                    return response
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
    return HttpResponse('')


def send_adaptive_slicing_config(request, tenant_id):
    if request.POST:
        tenant = get_object_or_404(Tenant, pk=tenant_id)

        if tenant.controller.controller_type == Controller.ControllerType.EMPOWER:
            active = request.POST['active']
            app = request.POST['app']
            min_quantum = request.POST['min_quantum']
            max_quantum = request.POST['max_quantum']
            inc_rate = request.POST['inc_rate']
            dec_rate = request.POST['dec_rate']

            url = 'http://' + tenant.controller.ip_addr + ':' + tenant.controller.port + '/api/v1/tenants/' + \
                  tenant.long_id + '/components/' + app

            payload = {
                'version': '1.0',
                'params': {
                    "active": False
                }
            }

            if active == 'true':
                payload['params']['active'] = True
                payload['params']['minimum_quantum'] = int(min_quantum)
                payload['params']['maximum_quantum'] = int(max_quantum)
                payload['params']['quantum_increase_rate'] = inc_rate
                payload['params']['quantum_decrease_rate'] = dec_rate
            try:
                r = requests.put(url, json=payload, auth=(tenant.controller.user, tenant.controller.password))
                if r.status_code != 204:
                    response = JsonResponse({"error": "Configuration not sent to the controller!"})
                    response.status_code = r.status_code
                    return response
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
    return HttpResponse('')


def tenant_data(request, tenant_id):
    crr_tenant = get_object_or_404(Tenant, pk=tenant_id)

    # Getting JSON descriptor from controller
    try:
        if crr_tenant.controller.controller_type == Controller.ControllerType.EMPOWER:
            url_addr = 'http://' + crr_tenant.controller.ip_addr + ':' + crr_tenant.controller.port + '/api/v1/tenants'
            r = requests.get(url_addr)
            if r.status_code == 200:
                topology = parse_topology_from_empower(r.json(), crr_tenant.long_id)
                traffic_rules = parse_traffic_rules_from_empower(r.json(), crr_tenant.long_id)
                slices = parse_slices_from_empower(r.json(), crr_tenant.long_id)
                apps = parse_apps_from_empower(r.json(), crr_tenant.long_id)
    except requests.exceptions.RequestException as e:
        topology = None
        traffic_rules = []
        slices = []
        apps = []
        # raise SystemExit(e)
    return JsonResponse({
        'topology': topology,
        'traffic_rules': traffic_rules,
        'slices': slices,
        'apps': apps
    })
