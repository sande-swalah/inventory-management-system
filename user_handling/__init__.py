def register_blueprints(app):
    from user_handling.MVC_architecture.controllers.user_routes import user_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/api/users")


def create_app_for_user_handling(app):
    register_blueprints(app)

    return app

    
