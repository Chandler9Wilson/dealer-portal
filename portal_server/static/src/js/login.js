function redirect () {
  document.location.href = '/home/'
}

function sendToken (idToken) {
  var myInit = {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
    credentials: 'same-origin',
    body: JSON.stringify({
      idtoken: idToken
    })
  }
  window.fetch('/gconnect/', myInit).then(function (response) {
    if (response.ok) {
      setTimeout(redirect, 200)
      // TODO find a better way to return this if statement
      return response
    }
    throw new Error('Network response was not ok.')
  })
}

// callback for google sign-in state change
function onSignIn (googleUser) {
  if (logoutFirst) {
    gapi.auth2.getAuthInstance().signOut()
    // prevents a signOut loop
    logoutFirst = undefined
  } else {
    var idToken = googleUser.getAuthResponse().id_token
    sendToken(idToken)
  }
}
