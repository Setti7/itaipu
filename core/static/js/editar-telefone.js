var last_value
var tel_input = $('#editar-telefone')
var animation = $('#animation-telefone')

tel_input.on('click touchstart mouseover', function () {

  last_value = this.value

  $(this).click(function () {
    $(this).select()
  })

  // rodando animação
  animation.removeClass('hidden')
})

tel_input.mouseout(function () {

  var tel_form = $('#editar-telefone-form')
  var tel_url = tel_form.attr('action')
  var tel_data = tel_form.serialize()
  var input = $(this)

  // Validação
  if (this.value.length <= 7 || this.value.length > 13) {
    input.val(last_value)

  } else {

    if (last_value === this.value) {

    } else {

      $.ajax({
        type: 'POST',
        url: tel_url,
        data: tel_data,
        dataType: 'json',
        success: function (data) {

          if (!data.success) {
            input.val(last_value)
            input.addClass('text-danger')
            alert(data.msg)

          } else if (data.success) {
            input.removeClass('text-danger')
          }
        },
      })
    }
  }

  // parando animação
  animation.addClass('hidden')
})

$('#editar-telefone-form').submit(function (e) {
  e.preventDefault()
})