const path = require('path')

const config = {
  entry: './src/js/directory.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'dealer_portal.bundle.js'
  },
  resolve: {
    extensions: ['.js', '.css']
  }
}

module.exports = config
