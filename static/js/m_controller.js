$('#form-modal').on('shown.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var titulo = button.data('titulo');
    var url = button.data('url');
    var action = button.data('action');
    var modulo = button.data('modulo');

    var modal = $(this);
    var form = modal.find('form');

    modal.find('.modal-title').html(titulo);
    modal.find('.modal-body p').html("");

    if (action == '@@open-object' || action == '@@list-all'){
        modal.find('#btn-save').hide();
    }else{
        modal.find('#btn-save').show();
    }

    if(modulo=='atividades'){
        form.attr('action', url+'?action='+action);
        param = {
            'action': action
        }
        run(url, param)
    }

    if(modulo=='acoes'){
        if(action=='@@list-all'){
            form.attr('action', url+'?action=@@update');
        }else{
            form.attr('action', url+'?action='+action);
        }
        param = {
            'action': action
        }
        run(url, param)
    }
});


function enable_button_and_save(url){
    $('form').attr('action', url);
    $('#btn-save').show();
}


function run(url, param) {
	$.ajax({
		url: url,
		type : "GET",
        data : param,
        contentType : "application/josn; charset=utf-8",
        success : function(data) {
        	 $('.modal-body p').html(data.result);
        },
        error : function(xhr , errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
	});
}