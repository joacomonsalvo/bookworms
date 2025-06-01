"""
Configuración global de la aplicación
Maneja URLs de DB, keys de APIs, etc.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    # BetterAuth Configuration
    BETTER_AUTH_SECRET = os.getenv('BETTER_AUTH_SECRET')
    BETTER_AUTH_URL = os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')
    
    # Resend Configuration
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@bookworms.com')
    
    # External APIs
    BOOKS_API_URL = os.getenv('BOOKS_API_URL', 'https://www.googleapis.com/books/v1')
    BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')
    
    # Application Settings
    ITEMS_PER_PAGE = 20
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    @staticmethod
    def validate_config():
        """Valida que las configuraciones críticas estén presentes"""
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
            'RESEND_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
