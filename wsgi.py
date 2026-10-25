"""
CareerIQ - WSGI Entrypoint for Production Serving
Works with Gunicorn, Waitress, uWSGI, and cloud platforms.
"""

from app import app

if __name__ == "__main__":
    from waitress import serve
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] CareerIQ Production WSGI Server running on port {port}...")
    serve(app, host="0.0.0.0", port=port)
