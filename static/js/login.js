function sendToken (idToken) {
  var myInit = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify({
      idtoken: idToken
    })
  }
  window.fetch('/gconnect?state={{STATE}}', myInit).then(
    function (response) {
      if (response.ok) {
        var div = document.getElementById('result')
        var responseMessage = 'Login Successful!</br>' + response + '</br>Redirecting...'
        div.insertAdjacentHTML('beforeend', responseMessage)
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
    window.location.href = '/home'
  }
}
