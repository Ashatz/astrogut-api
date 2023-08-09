def register_route_endpoints(app):
    
    # Default health check function.
    def health():
        from flask import render_template
        return render_template('health.html')

    # Register default routes.
    app.add_url_rule('/', 'get', health)
    app.add_url_rule('/health', 'health', health)

    # Register custom routes.
    from . import reporters
    app.register_blueprint(reporters.bp, url_prefix=reporters.prefix)