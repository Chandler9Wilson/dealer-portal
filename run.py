from portal_server import app

app.run(
    port=8000,
    # TODO investigate why threaded needs to be turned on for back to work?
    threaded=True,
    debug=True
)
