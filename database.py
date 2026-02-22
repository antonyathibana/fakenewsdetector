"""
Database Module for Fake News Detection Web Application
Handles SQLite database for storing prediction history
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import config


def init_db():
    """
    Initialize the database with required tables
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            is_url INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✓ Database initialized successfully")


def save_prediction(text, prediction, confidence, is_url=False):
    """
    Save a prediction to the database
    
    Args:
        text: Input text or URL
        prediction: 'FAKE' or 'REAL'
        confidence: Confidence score (0-100)
        is_url: Whether input was a URL
    
    Returns:
        int: ID of the inserted record
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (text, prediction, confidence, is_url)
        VALUES (?, ?, ?, ?)
    ''', (text, prediction, confidence, 1 if is_url else 0))
    
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return prediction_id


def get_history(limit=50, offset=0):
    """
    Get prediction history
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        list: List of prediction records
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, text, prediction, confidence, is_url, created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_prediction_by_id(prediction_id):
    """
    Get a specific prediction by ID
    
    Args:
        prediction_id: ID of the prediction
    
    Returns:
        dict: Prediction record or None
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, text, prediction, confidence, is_url, created_at
        FROM predictions
        WHERE id = ?
    ''', (prediction_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None


def get_total_count():
    """
    Get total number of predictions
    
    Returns:
        int: Total count
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM predictions')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count


def clear_history():
    """
    Clear all prediction history
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM predictions')
    conn.commit()
    conn.close()
    
    print("✓ History cleared successfully")


def get_stats():
    """
    Get prediction statistics
    
    Returns:
        dict: Statistics dictionary
    """
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total predictions
    cursor.execute('SELECT COUNT(*) FROM predictions')
    total = cursor.fetchone()[0]
    
    # Fake vs Real count
    cursor.execute('''
        SELECT prediction, COUNT(*) as count
        FROM predictions
        GROUP BY prediction
    ''')
    
    stats = dict(cursor.fetchall())
    
    # Average confidence
    cursor.execute('SELECT AVG(confidence) FROM predictions')
    avg_confidence = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total': total,
        'fake': stats.get('FAKE', 0),
        'real': stats.get('REAL', 0),
        'avg_confidence': round(avg_confidence, 2)
    }


# Initialize database when module is imported
if __name__ == "__main__":
    init_db()
else:
    # Initialize in background
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization: {e}")

