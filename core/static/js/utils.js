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

function capitalize (string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

function response (success, text, timeout = 3000) {
  var alert_banner = $('#alert-banner')

  alert_banner.html(text)
  alert_banner.fadeIn()

  if (success === true) {
    alert_banner.removeClass('alert-danger')
    alert_banner.addClass('alert-success')
  } else {
    alert_banner.removeClass('alert-success')
    alert_banner.addClass('alert-danger')
  }

  setTimeout(function () {
    alert_banner.fadeOut()
  }, timeout)
}