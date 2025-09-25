const { merge } = require('webpack-merge');
const path = require('path');
const common = require('./webpack.common.js');
const Dotenv = require('dotenv-webpack');
module.exports = merge(common, {
    mode: 'production',
   output: {
        path: path.resolve(__dirname, 'public'), // 👈 acá define la carpeta destino
        filename: 'bundle.js',
        publicPath: '/'
    },
    plugins: [
        new Dotenv({
            safe: true,
            systemvars: true
        })
    ]
});
