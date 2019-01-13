function enable_edit(id) {

	// definindo variáveis
	var btn_salvar = $('#edit-' + id);
	var btn_cancelar = $('#del-' + id);
	var btn_blacklist = $('#blacklist-' + id);

	// alterando data-action dos botoes sendo:
	// [edit] -> [salvar] e [delete] -> [cancelar]
	btn_salvar.attr('data-action', 'salvar');
	btn_cancelar.attr('data-action', 'cancelar');

	// habilitando todos os inputs do form
	$('#form-' + id + " :input").each(function () {
		var input = $(this);
		input.removeAttr("disabled");
	});

	// Alterando os botões:
	// Botao de editar -> Salvar
	$(btn_salvar).html("<span class='octicon octicon-check'></span> Salvar");
	$(btn_salvar).removeClass("btn-outline-secondary");
	$(btn_salvar).addClass("btn-success");

	// botao de excluir -> Cancelar
	$(btn_cancelar).html("<span class='octicon octicon-x'></span> Cancelar");
	$(btn_cancelar).removeClass("btn-outline-secondary");
	$(btn_cancelar).addClass("btn-danger");

	// botao de proibir é exibido
	$(btn_blacklist).removeClass("hidden");

}

function disable_edit(id, reload) {
	if (typeof (reload) === 'undefined') reload = true;

	// definindo variavéis
	var form = $('#form-' + id);
	var btn_edit = $('#edit-' + id);
	var btn_del = $('#del-' + id);
	var btn_blacklist = $('#blacklist-' + id);
	var field_group = $('#field-group-' + id);
	var field_group_childrens = ' #field-group-' + id + ' > *';

	// alterando data-action dos botoes sendo:
	// [salvar] -> [edit] e [cancelar] -> [delete]
	btn_edit.attr('data-action', 'edit');
	btn_del.attr('data-action', 'delete');

	// recarregando elementos (apenas os inputs e o csrf_token)
	if (reload) {
		field_group.load(location.href + field_group_childrens);
	}

	// desabilitando todos os inputs do form (desconsiderando os botoes)
	$('#form-' + id + " :input").each(function () {
		var input = $(this);

		if (typeof (input.attr('data-action')) === 'undefined') {
			input.attr("disabled", true);

		} else {
			input.attr("disabled", false);
		}
	});

	// Alterando os botões:
	// Botao de salvar -> editar
	$(btn_edit).html("<span class='octicon octicon-pencil'></span> Editar");
	$(btn_edit).removeClass("btn-success");
	$(btn_edit).addClass("btn-outline-secondary");

	// botao de cancelar -> excluir
	$(btn_del).html("<span class='octicon octicon-trashcan'></span> Excluir");
	$(btn_del).removeClass("btn-danger");
	$(btn_del).addClass("btn-outline-secondary");

	// botao de proibir é escondido
	$(btn_blacklist).addClass("hidden");
}

function error_alert(error) {
	var alert = $("#error-alert");

	alert.html(error);
	alert.removeClass('hidden');
}

function capitalize(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function save_edit(id, form) {

	// validando form e ressaltando erros
	form.validate({
		onfocusout: false,
		onkeyup: false,

		messages: {
			nome: "Digite o nome do visitante",
			data: "Escolha uma data"
		},

		errorPlacement: function (error, element) {
			var id = element.attr('data-id');
			var nome = element.attr('name');

			var label = $(`span[data-id=${id}][data-name=${nome}]`);

			// adicionar classe de invalido caso ainda nao tenha
			if (!element.hasClass('is-invalid')) {
				element.addClass('is-invalid');
			}

			label.addClass('error');
			label.html(error)
		},

		success: function (label, element) {

			var id = element.getAttribute('data-id');
			var nome = element.getAttribute('name');

			var elem_label = $(`span[data-id=${id}][data-name=${nome}]`);

			//remover classe de invalido caso ainda tenha
			if (element.classList.contains('is-invalid')) {
				element.classList.remove("is-invalid");
			}

			elem_label.removeClass('error');
			elem_label.html(capitalize(nome));
		},

	});

	// enviando form e desabilitando campos
	if (form.valid()) {

		// preparando animação
		var animation = '#animation-' + id;
		$(animation).removeClass("hidden");

		// pegar info dos campos
		var url = form.attr('action');
		var data = form.serialize();

		disable_edit(id, false);

		// enviar form
		$.ajax({
			type: "POST",
			url: url,
			data: data,
			dataType: 'json',
			success: function (data) {
				if (!data.success) {
					error_alert("Houve um erro inesperado ao deletar esse visitante. Tente novamente.");
				} else {

					// se entrada for alterada com sucesso, atualizar o label "autorizado por" com o nome do usuário
					var auth_label = $(`small[data-id=${id}]`);
					var user = auth_label.attr('data-name');

					auth_label.html("Autorizado por:<br>" + user)
				}
			}
		});
		$(animation).addClass("hidden");
	}
}

function remove_entry(id, form, action) {

	// preparando animação
	var animation = '#animation-' + id;
	$(animation).removeClass("hidden");

	// pegando id da coluna especifica a esse card
	var col_id = '#col-' + id;

	// pegando infos dos campos
	var url = form.attr('action');

	// Precisa habilitar inputs para fazer serializing dos campos

	enable_edit(id);
	var data = form.serialize();
	disable_edit(id);

	// blacklist ou delete
	data += '&' + action + '=true';

	$.ajax({
		type: "POST",
		url: url,
		data: data,
		dataType: 'json',
		success: function (data) {
			if (data.success) {
				$(col_id).fadeOut();
			} else {

				if (action === 'delete') {
					alert("Houve um erro ao deletar esse visitante.");

				} else if (action === 'blacklist') {
					alert("Houve um erro ao proibir esse visitante.");
				}

				$(animation).addClass("hidden");
			}
		}
	});
}


$(".js-btn").click(function () {

	// id que identifica a form/botoes/inputs/etc
	var id = this.getAttribute('data-id');
	var action = this.getAttribute('data-action');

	var form = $('#form-' + id);

	if (action === 'edit') {
		enable_edit(id);

	} else if (action === 'cancelar') {
		disable_edit(id);

	} else if (action === 'salvar') {
		save_edit(id, form)

	} else if (action === 'blacklist') {
		remove_entry(id, form, action)

	} else if (action === 'delete') {
		remove_entry(id, form, action)
	}
});


