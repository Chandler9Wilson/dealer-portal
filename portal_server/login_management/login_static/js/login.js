// This logs out the user anytime login is visited
// TODO find a better solution this seems less than ideal
window.onbeforeunload = function (e) {
  gapi.auth2.getAuthInstance().signOut()
}

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
  var idToken = googleUser.getAuthResponse().id_token
  sendToken(idToken)
}

function onFailure (error) {
  console.log(error)
}

function renderButton () {
  gapi.signin2.render('my-signin2', {
    'scope': 'profile email',
    'width': 'auto',
    'height': 50,
    'longtitle': true,
    'theme': 'dark',
    'onsuccess': onSignIn,
    'onfailure': onFailure
  })
}
