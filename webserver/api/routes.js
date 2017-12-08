module.exports =  (app) => {
    var controller = require('./controller');
    app.route('/search').get(controller.handleQuery);
    app.route('/get_health').get()
    app.route('*').get(controller.fofhandler);    
}