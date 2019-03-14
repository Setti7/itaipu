var aviso_card = $('.aviso-card-js')
var url = $('#aviso-lido-url').attr('data-url')

aviso_card.each(function () {

  let el = $(this)
  let hover_card = el.children()

  if (el.attr('data-viewed') === 'true') {
    apply_read_style(el, hover_card)

  } else {

    // showing badge of new notice
    not_read_badge = el.find('.not-read-badge-js')
    not_read_badge.removeClass('hidden')

    let modal_id = hover_card.attr('data-id')
    let modal = $(`#readMoreModal-${modal_id}`)

    modal.on('hidden.bs.modal', function (e) {
      mark_as_read(modal_id, el, hover_card)
    })

  }
})

function apply_read_style (el, hover_card) {

  // showing badge of already read
  already_read_badge = el.find('.already-read-badge-js')
  already_read_badge.removeClass('hidden')
  hover_card.addClass('card-hover')

  // Cards with "card-hover" class mess up the screen when its modal show up.
  // To fix his we remove this class when the button to call the modal is
  // clicked, and add it again after the modal is hidden.
  hover_card.on('click', function () {

    hover_card.removeClass('card-hover')

    let modal_id = hover_card.attr('data-id')
    let modal = $(`#readMoreModal-${modal_id}`)

    modal.on('hidden.bs.modal', function (e) {
      hover_card.addClass('card-hover')
    })
  })
}

function mark_as_read (id, el, hover_card) {

  $.ajax({
    type: 'POST',
    url: url,
    data: 'aviso_id=' + id,
    dataType: 'json',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    },
    success: function (data) {

      if (data.success) {
        console.log('sucesso!')

        // showing badge of already read and applying custom classes
        not_read_badge = el.find('.not-read-badge-js')
        not_read_badge.addClass('hidden')
        el.attr('data-viewed', true)

        apply_read_style(el, hover_card)
      }
    },
  })
}

function getCookie (name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i])
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}