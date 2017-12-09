module.exports =  (app) => {
    var controller = require('./controller')
    app.route('/search').get(controller.handleQuery)
    app.route('/get_health').get(controller.handleHealth)
    app.route('/searchcache').get(controller.handleCacheSearch)
    app.route('*').get(controller.fofhandler)
}
