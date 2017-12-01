module.exports =  (app) => {
    var controller = require('./controller');
    app.route('/:query').get(controller.handleQuery);
}