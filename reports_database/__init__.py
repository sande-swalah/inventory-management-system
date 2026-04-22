def register_blueprints(app):
    from reports_database.MVC_architecture.controllers.report_routes import report_blueprint

    app.register_blueprint(report_blueprint, url_prefix="/api")