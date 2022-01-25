var tid;

// topology global vars
var nodes, edges, network, topology;
var nodesArray = [];
var edgesArray = [];

var apps_columns = [{
    field: 'id',
    title: '#'
},{
    field: 'jitter_ms',
    title: 'MAX Jitter (ms)'
},{
    field: 'rtt_ms',
    title: 'E2E MAX Latency (ms)'
}]

var traffic_rules_columns = [{
    field: 'id',
    title: '#'
}, {
    field: 'label',
    title: 'Label'
}, {
    field: 'dscp',
    title: 'DSCP'
}, {
    field: 'match',
    title: 'Match'
}, {
    field: 'priority',
    title: 'Priority'
}]

var slices_columns = [{
    field: 'id',
    title: '#'
}, {
    field: 'wtp',
    title: 'WTP'
}, {
    field: 'dscp',
    title: 'DSCP'
}, {
    field: 'amsdu',
    title: 'AMSDU'
}, {
    field: 'quantum',
    title: 'Quantum'
}, {
    field: 'scheduler',
    title: 'Scheduler'
}]

$('#polling_interval_selector').on('change', function () {
    // clear interval
    clearInterval(tid)
    if (parseInt(this.value) >= 5) {
        // set interval
        tid = setInterval(network_sync_timer, this.value * 1000);
    }
});

function network_sync_timer() {
    console.log('Network Sync...')
    getData()
}

function abortTimer() { // to be called when you want to stop the timer
    clearInterval(tid);
}

function getData() {
    $.ajax({
        url: 'data/',
        type: "GET",
        dataType: "json",
        success: function (data) {
            topology = data['topology'];
            traffic_rules = data['traffic_rules'];
            slices = data['slices'];
            apps = data['apps'];
            $('#table_traffic_rules').bootstrapTable("destroy");
            $('#table_slices').bootstrapTable("destroy");
            $('#table_apps').bootstrapTable("destroy");
            $('#table_traffic_rules').bootstrapTable({
                columns: traffic_rules_columns,
                data: traffic_rules
            });
            $('#table_slices').bootstrapTable({
                columns: slices_columns,
                data: slices
            });
            $('#table_apps').bootstrapTable({
                columns: apps_columns,
                data: apps
            });
            reloadNetwork();
        }
    });
}

function startNetwork() {
    // create an array with nodes
    nodes = new vis.DataSet(nodesArray);

    // create an array with edges
    edges = new vis.DataSet(edgesArray);

    // create a network
    var container = document.getElementById('my_network');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    network = new vis.Network(container, data, options);
}

function startLegend() {
    // create an array with nodes
    div_width = $("#my_legend").width();
    legendNodes = [
        {id: 10001, x: 0, y: 0, shape: 'dot', color: '#97C2FC'},
        {id: 10002, x: 100, y: 0, shape: 'text', label: 'WTP (online)'},
        {id: 10003, x: 250, y: 0, shape: 'dot', color: '#FB7E81'},
        {id: 10004, x: 350, y: 0, shape: 'text', label: 'WTP (offline)'},
        {id: 10005, x: 500, y: 0, shape: 'dot', color: '#000000'},
        {id: 10006, x: 600, y: 0, shape: 'text', label: 'STA node'},
        {id: 10007, x: 750, y: 0, shape: 'text', label: ''},
        {id: 10008, x: 850, y: 0, shape: 'text', label: ''},
        {id: 10009, x: 950, y: 0, shape: 'text', label: 'Wired Link'},
        {id: 10010, x: 1100, y: 0, shape: 'text', label: ''},
        {id: 10011, x: 1200, y: 0, shape: 'text', label: ''},
        {id: 10012, x: 1300, y: 0, shape: 'text', label: 'Wireless Link'}
    ];
    nodes = new vis.DataSet(legendNodes);

    // create an array with edges
    legendEdges = [
        {'from': 10007, 'to': 10008},
        {'from': 10010, 'to': 10011, 'color': {'color': 'black'}, 'dashes': 'true'}
    ];
    edges = new vis.DataSet(legendEdges);

    // create a network
    var container = document.getElementById('my_legend');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        nodes: {
            fixed: true,
            font: {
                face: 'Helvetica Neue',
                size: 20
            }
        },
        interaction: {
            zoomView: false,
            dragView: false,
            dragNodes: false

        },
    };
    network = new vis.Network(container, data, options);
}

function reloadNetwork() {
    nodes.clear();
    edges.clear();
    if (topology) {
        nodesArray = topology['nodes'];
        edgesArray = topology['edges'];
        nodes.add(nodesArray);
        edges.add(edgesArray);

        // Adding WTP options to selector
        if ('wtps' in topology) {
            topology['wtps'].forEach(function (entry) {
                if ($("#inputWTP option[value='" + entry['addr'] + "']").length == 0) {
                    $('#inputWTP').append("<option value='" + entry['addr'] + "'>" + entry['label'] + "</option>");
                }
            });
        }
    }
}


function initTables() {
    $('#table_traffic_rules').bootstrapTable({columns: traffic_rules_columns});
    $('#table_slices').bootstrapTable({columns: slices_columns});
}

initTables();
startLegend();
startNetwork();