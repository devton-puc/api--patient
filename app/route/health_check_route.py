from flask import Flask, jsonify

class HealthCheckRoute:
    """Classe responsável por definir a rota de health check."""

    def init_routes(self, app):
        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"message": "API is running"}), 200
