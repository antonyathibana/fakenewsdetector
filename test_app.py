"""
Test Suite for Fake News Detection Application
Run tests with: pytest test_app.py -v
"""

import pytest
import sys
import os
import tempfile
import sqlite3
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules to test
import preprocess_data
import database


class TestPreprocessData:
    """Test cases for preprocess_data module"""
    
    def test_preprocess_text_basic(self):
        """Test basic text preprocessing"""
        text = "This is a TEST message with URL http://example.com and email test@test.com"
        result = preprocess_data.preprocess_text(text)
        
        # Check that preprocessing happened
        assert isinstance(result, str)
        # URL and email should be removed
        assert 'http' not in result
        assert '@' not in result
        # Should be lowercase
        assert result == result.lower()
    
    def test_preprocess_text_empty(self):
        """Test preprocessing with empty/NaN input"""
        result = preprocess_data.preprocess_text("")
        assert result == ""
        
        result = preprocess_data.preprocess_text(None)
        assert result == ""
    
    def test_preprocess_text_punctuation(self):
        """Test that punctuation is removed"""
        text = "Hello, World! How are you? I'm fine..."
        result = preprocess_data.preprocess_text(text)
        
        # Punctuation should be removed
        assert ',' not in result
        assert '!' not in result
        assert '?' not in result
        assert '.' not in result
    
    def test_preprocess_text_numbers(self):
        """Test that numbers are removed"""
        text = "There are 123 tests and 456 examples"
        result = preprocess_data.preprocess_text(text)
        
        # Numbers should be removed
        assert '123' not in result
        assert '456' not in result
    
    def test_stemmer_available(self):
        """Test that stemmer is available"""
        assert preprocess_data.stemmer is not None
    
    def test_stopwords_defined(self):
        """Test that stopwords are defined"""
        assert isinstance(preprocess_data.STOPWORDS, set)
        assert len(preprocess_data.STOPWORDS) > 0
        # Check common stopwords
        assert 'the' in preprocess_data.STOPWORDS
        assert 'is' in preprocess_data.STOPWORDS
        assert 'and' in preprocess_data.STOPWORDS


class TestDatabase:
    """Test cases for database module"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        # Create temp file
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        # Store original path and update config
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = path
        
        # Initialize database
        database.init_db()
        
        yield path
        
        # Cleanup
        config.DATABASE_PATH = original_path
        if os.path.exists(path):
            os.remove(path)
    
    def test_init_db(self, temp_db):
        """Test database initialization"""
        assert os.path.exists(temp_db)
        
        # Check table exists
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert 'predictions' in tables
    
    def test_save_prediction(self, temp_db):
        """Test saving a prediction"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        pred_id = database.save_prediction(
            text="Test news article",
            prediction="FAKE",
            confidence=85.5,
            is_url=False
        )
        
        assert pred_id is not None
        assert pred_id > 0
        
        config.DATABASE_PATH = original_path
    
    def test_get_history(self, temp_db):
        """Test retrieving prediction history"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        # Import fresh to avoid cached connection
        import importlib
        importlib.reload(database)
        
        # Save some predictions
        database.save_prediction("Text 1", "FAKE", 80.0, False)
        database.save_prediction("Text 2", "REAL", 90.0, False)
        
        # Get history
        history = database.get_history(limit=10, offset=0)
        
        assert len(history) == 2
        # Just verify both texts exist (order may vary)
        texts = [h['text'] for h in history]
        assert "Text 1" in texts
        assert "Text 2" in texts
        
        config.DATABASE_PATH = original_path
    
    def test_get_prediction_by_id(self, temp_db):
        """Test retrieving specific prediction"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        # Save prediction
        pred_id = database.save_prediction("Test text", "FAKE", 75.0, False)
        
        # Retrieve it
        prediction = database.get_prediction_by_id(pred_id)
        
        assert prediction is not None
        assert prediction['text'] == "Test text"
        assert prediction['prediction'] == "FAKE"
        
        config.DATABASE_PATH = original_path
    
    def test_get_total_count(self, temp_db):
        """Test getting total prediction count"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        # Initially should be 0
        count = database.get_total_count()
        assert count == 0
        
        # Add predictions
        database.save_prediction("Text 1", "FAKE", 80.0, False)
        database.save_prediction("Text 2", "REAL", 90.0, False)
        
        count = database.get_total_count()
        assert count == 2
        
        config.DATABASE_PATH = original_path
    
    def test_clear_history(self, temp_db):
        """Test clearing prediction history"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        # Add predictions
        database.save_prediction("Text 1", "FAKE", 80.0, False)
        database.save_prediction("Text 2", "REAL", 90.0, False)
        
        # Clear
        database.clear_history()
        
        # Should be empty
        count = database.get_total_count()
        assert count == 0
        
        config.DATABASE_PATH = original_path
    
    def test_get_stats(self, temp_db):
        """Test getting prediction statistics"""
        import config
        original_path = config.DATABASE_PATH
        config.DATABASE_PATH = temp_db
        
        # Add predictions
        database.save_prediction("Text 1", "FAKE", 80.0, False)
        database.save_prediction("Text 2", "REAL", 90.0, False)
        database.save_prediction("Text 3", "FAKE", 70.0, False)
        
        stats = database.get_stats()
        
        assert stats['total'] == 3
        assert stats['fake'] == 2
        assert stats['real'] == 1
        assert stats['avg_confidence'] > 0
        
        config.DATABASE_PATH = original_path


class TestConfig:
    """Test cases for configuration"""
    
    def test_config_exists(self):
        """Test that config module can be imported"""
        import config
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'DATABASE_PATH')
        assert hasattr(config, 'MODEL_PATH')
        assert hasattr(config, 'VECTORIZER_PATH')
    
    def test_config_values(self):
        """Test config values are set"""
        import config
        assert config.SECRET_KEY is not None
        assert len(config.SECRET_KEY) > 0


class TestAppImports:
    """Test cases for app module imports"""
    
    def test_app_imports(self):
        """Test that app module can be imported"""
        # This will fail if there are import errors
        import app
        assert app is not None
    
    def test_app_has_required_functions(self):
        """Test that app has required functions"""
        import app
        assert hasattr(app, 'predict_news')
        assert hasattr(app, 'load_model')
        assert hasattr(app, 'extract_text_from_url')


class TestModelLoading:
    """Test cases for model loading (if available)"""
    
    def test_model_files_exist(self):
        """Test that model files exist"""
        import config
        model_exists = os.path.exists(config.MODEL_PATH)
        vectorizer_exists = os.path.exists(config.VECTORIZER_PATH)
        
        if model_exists and vectorizer_exists:
            # If files exist, try loading them
            import pickle
            with open(config.MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            with open(config.VECTORIZER_PATH, 'rb') as f:
                vectorizer = pickle.load(f)
            
            assert model is not None
            assert vectorizer is not None
        else:
            pytest.skip("Model files not available")


class TestFlaskApp:
    """Test cases for Flask application"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        # Check if model files exist, skip if not
        import config
        if not os.path.exists(config.MODEL_PATH):
            pytest.skip("Model files not available")
        
        from app import app
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            yield client
    
    def test_index_route(self, client):
        """Test index route"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_predict_route_empty(self, client):
        """Test predict route with empty input"""
        response = client.post('/predict', data={'news_text': ''})
        # Should redirect back to index with flash message
        assert response.status_code in [200, 302]
    
    def test_predict_route_with_text(self, client):
        """Test predict route with valid text"""
        # Use a longer text to get a valid prediction
        long_text = """
        The President announced today that the government will implement new policies to address 
        climate change and environmental protection. The new legislation aims to reduce carbon 
        emissions by 50% over the next decade. Environmental groups have praised the initiative 
        while some industry leaders expressed concerns about the economic impact. The bill is 
        expected to pass through Congress next month after extensive negotiations.
        """
        response = client.post('/predict', data={
            'news_text': long_text
        })
        # Should return result page (200) or redirect (302) depending on prediction
        assert response.status_code in [200, 302]
    
    def test_history_route(self, client):
        """Test history route"""
        response = client.get('/history')
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

