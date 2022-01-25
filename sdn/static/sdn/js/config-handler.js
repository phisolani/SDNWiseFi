$(document).on('submit', '#form_send_slice_config', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'set_slice/',
        data: {
            wtp: $('#inputWTP').val(),
            dscp: $('#inputSliceDSCP').val(),
            quantum: $('#inputQuantum').val(),
            amsdu: $('#inputAMSDUToggle').prop("checked"),
            scheduler: $('#inputSliceScheduler').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            $('#div_response_message_management_config').removeClass('alert-danger');
            $('#div_response_message_management_config').addClass('alert-success');
            $('#p_message_response_management_config').text('Configuration successfully sent to the controller!')
            $('#div_response_message_management_config').show();
        },
        error: function (data) {
            $('#div_response_message_management_config').removeClass('alert-success');
            $('#div_response_message_management_config').addClass('alert-danger');
            $('#p_message_response_management_config').text('Request to the controller failed with status code: ' + data.status)
            $('#div_response_message_management_config').show();
        }
    });
})

$(document).on('submit', '#form_send_mcda_config', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'set_mcda/',
        data: {
            active: $('#inputMCDAToggle').prop("checked"),
            app: $('#inputMCDAHandoverAPP').val(),
            qos_channel_load_rate: $('#inputQoSChannelLoadRate').val(),
            qos_rssi: $('#inputQoSRSSI').val(),
            qos_expected_load: $('#inputQoSExpectedLoad').val(),
            qos_measured_load: $('#inputQoSMeasuredLoad').val(),
            qos_queueing_delay: $('#inputQoSQueueingDelay').val(),
            qos_association_status: $('#inputQoSAssociationStatus').val(),
            be_channel_load_rate: $('#inputBEChannelLoadRate').val(),
            be_rssi: $('#inputBERSSI').val(),
            be_expected_load: $('#inputBEExpectedLoad').val(),
            be_measured_load: $('#inputBEMeasuredLoad').val(),
            be_queueing_delay: $('#inputBEQueueingDelay').val(),
            be_association_status: $('#inputBEAssociationStatus').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            $('#div_response_message_brain_config').removeClass('alert-danger');
            $('#div_response_message_brain_config').addClass('alert-success');
            $('#p_message_response_brain_config').text('Configuration successfully sent to the controller!')
            $('#div_response_message_brain_config').show();
        },
        error: function (data) {
            $('#div_response_message_brain_config').removeClass('alert-success');
            $('#div_response_message_brain_config').addClass('alert-danger');
            $('#p_message_response_brain_config').text('Request to the controller failed with status code: ' + data.status)
            $('#div_response_message_brain_config').show();
        }
    });
})

$(document).on('submit', '#form_send_adaptive_slicing_config', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'set_adaptive_slicing/',
        data: {
            active: $('#inputAdaptiveSlicingToggle').prop("checked"),
            app: $('#inputAdaptiveSlicingAPP').val(),
            min_quantum: $('#inputAdaptiveSlicingMinQuantum').val(),
            max_quantum: $('#inputAdaptiveSlicingMaxQuantum').val(),
            inc_rate: $('#inputAdaptiveSlicingIncRate').val(),
            dec_rate: $('#inputAdaptiveSlicingDecRate').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            $('#div_response_message_brain_config').removeClass('alert-danger');
            $('#div_response_message_brain_config').addClass('alert-success');
            $('#p_message_response_brain_config').text('Configuration successfully sent to the controller!')
            $('#div_response_message_brain_config').show();
        },
        error: function (data) {
            $('#div_response_message_brain_config').removeClass('alert-success');
            $('#div_response_message_brain_config').addClass('alert-danger');
            $('#p_message_response_brain_config').text('Request to the controller failed with status code: ' + data.status)
            $('#div_response_message_brain_config').show();
        }
    });
})

$(function () {
    // bind change event to select
    $('#tenant_selector').on('change', function () {
        var url = $(this).val(); // get selected value
        if (url) { // require a URL
            window.location = url; // redirect
        }
        return false;
    });
});

$('#networkManagementModal').on('show.bs.modal', function () {
    $('#div_response_message_management_config').hide();
    $("#form_send_slice_config")[0].reset();
    $('#inputSliceDSCP').prop('selectedIndex',0);
    $("#inputAMSDUToggle").bootstrapToggle('off');
    $('#inputSliceScheduler').prop('selectedIndex',0);
    $('#inputWTP').prop('selectedIndex',0);
});

$('#networkBrainModal').on('show.bs.modal', function () {
    $('#div_response_message_brain_config').hide();
    $("#form_send_mcda_config")[0].reset();
    $("#form_send_adaptive_slicing_config")[0].reset();
    $("#inputMCDAToggle").bootstrapToggle('off');
    $("#inputAdaptiveSlicingToggle").bootstrapToggle('off');
    $('#div_mcda_fields').hide();
    $('#div_adaptive_slicing_fields').hide();
});


$("#inputMCDAToggle").change(function () {
    if ($(this).prop("checked") == true) {
        $('#div_mcda_fields').show();
    } else {
        $('#div_mcda_fields').hide();
    }
});

$("#inputAdaptiveSlicingToggle").change(function () {
    if ($(this).prop("checked") == true) {
        $('#div_adaptive_slicing_fields').show();
    } else {
        $('#div_adaptive_slicing_fields').hide();
    }
});