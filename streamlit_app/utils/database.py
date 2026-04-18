"""
Database Manager for Movie Review System
Handles persistent storage of reviews, history, and analytics
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

class DatabaseManager:
    """Manages SQLite database for review history and analytics"""
    
    def __init__(self, db_path: str = "movie_reviews.db"):
        """Initialize database connection"""
        self.db_path = Path(db_path)
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        
        # Users table (optional, for future multi-user support)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Reviews table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id TEXT PRIMARY KEY,
                user_id TEXT,
                movie_plot TEXT NOT NULL,
                plot_hash TEXT NOT NULL,
                persona TEXT NOT NULL,
                generated_review TEXT NOT NULL,
                validation_score REAL,
                predicted_persona TEXT,
                total_attempts INTEGER,
                success BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Batch reviews table (for "All 3 Personas")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS batch_reviews (
                batch_id TEXT PRIMARY KEY,
                user_id TEXT,
                movie_plot TEXT NOT NULL,
                plot_hash TEXT NOT NULL,
                total_personas INTEGER DEFAULT 3,
                success_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Analytics table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Create indexes for faster queries
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reviews_user 
            ON reviews(user_id, created_at DESC)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reviews_plot_hash 
            ON reviews(plot_hash)
        """)
        
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_batch_user 
            ON batch_reviews(user_id, created_at DESC)
        """)
        
        self.conn.commit()
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for movie plot to detect duplicates"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _generate_id(self, prefix: str = "rev") -> str:
        """Generate unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"
    
    def create_user(self, user_id: str) -> bool:
        """Create or update user"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, last_active)
                VALUES (?, CURRENT_TIMESTAMP)
            """, (user_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def save_review(self, user_id: str, movie_plot: str, persona: str, 
                   result: Dict) -> Optional[str]:
        """Save single review to database"""
        try:
            review_id = self._generate_id("rev")
            plot_hash = self._generate_hash(movie_plot)
            
            self.cursor.execute("""
                INSERT INTO reviews (
                    review_id, user_id, movie_plot, plot_hash, persona,
                    generated_review, validation_score, predicted_persona,
                    total_attempts, success
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review_id,
                user_id,
                movie_plot,
                plot_hash,
                persona,
                result.get('final_review', ''),
                result.get('validation_score', 0.0),
                result.get('predicted_persona', ''),
                result.get('total_attempts', 0),
                result.get('success', False)
            ))
            
            self.conn.commit()
            return review_id
            
        except Exception as e:
            print(f"Error saving review: {e}")
            return None
    
    def save_batch_review(self, user_id: str, movie_plot: str, 
                         results: Dict) -> Optional[str]:
        """Save batch review (All 3 Personas) to database"""
        try:
            batch_id = self._generate_id("batch")
            plot_hash = self._generate_hash(movie_plot)
            
            # Save batch record
            success_count = sum(1 for r in results.get('results', {}).values() 
                              if r.get('success'))
            
            self.cursor.execute("""
                INSERT INTO batch_reviews (
                    batch_id, user_id, movie_plot, plot_hash,
                    total_personas, success_count
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                batch_id,
                user_id,
                movie_plot,
                plot_hash,
                3,
                success_count
            ))
            
            # Save individual reviews
            for persona_name, persona_result in results.get('results', {}).items():
                review_id = self._generate_id("rev")
                
                self.cursor.execute("""
                    INSERT INTO reviews (
                        review_id, user_id, movie_plot, plot_hash, persona,
                        generated_review, validation_score, predicted_persona,
                        total_attempts, success
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    review_id,
                    user_id,
                    movie_plot,
                    plot_hash,
                    persona_name,
                    persona_result.get('final_review', ''),
                    persona_result.get('validation_score', 0.0),
                    persona_result.get('predicted_persona', ''),
                    persona_result.get('total_attempts', 0),
                    persona_result.get('success', False)
                ))
            
            self.conn.commit()
            return batch_id
            
        except Exception as e:
            print(f"Error saving batch review: {e}")
            return None
    
    def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's review history"""
        try:
            self.cursor.execute("""
                SELECT * FROM reviews
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
            
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error getting history: {e}")
            return []
    
    def get_review_by_id(self, review_id: str) -> Optional[Dict]:
        """Get specific review by ID"""
        try:
            self.cursor.execute("""
                SELECT * FROM reviews WHERE review_id = ?
            """, (review_id,))
            
            row = self.cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            print(f"Error getting review: {e}")
            return None
    
    def check_duplicate_plot(self, movie_plot: str, user_id: str = None) -> Optional[Dict]:
        """Check if plot was already processed"""
        try:
            plot_hash = self._generate_hash(movie_plot)
            
            if user_id:
                self.cursor.execute("""
                    SELECT * FROM reviews
                    WHERE plot_hash = ? AND user_id = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (plot_hash, user_id))
            else:
                self.cursor.execute("""
                    SELECT * FROM reviews
                    WHERE plot_hash = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (plot_hash,))
            
            row = self.cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return None
    
    def get_statistics(self, user_id: str = None) -> Dict:
        """Get system/user statistics"""
        try:
            stats = {}
            
            if user_id:
                # User-specific stats
                self.cursor.execute("""
                    SELECT 
                        COUNT(*) as total_reviews,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_reviews,
                        AVG(validation_score) as avg_score,
                        AVG(total_attempts) as avg_attempts
                    FROM reviews
                    WHERE user_id = ?
                """, (user_id,))
            else:
                # Global stats
                self.cursor.execute("""
                    SELECT 
                        COUNT(*) as total_reviews,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_reviews,
                        AVG(validation_score) as avg_score,
                        AVG(total_attempts) as avg_attempts
                    FROM reviews
                """)
            
            row = self.cursor.fetchone()
            if row:
                stats = dict(row)
            
            # Persona distribution
            if user_id:
                self.cursor.execute("""
                    SELECT persona, COUNT(*) as count
                    FROM reviews
                    WHERE user_id = ?
                    GROUP BY persona
                """, (user_id,))
            else:
                self.cursor.execute("""
                    SELECT persona, COUNT(*) as count
                    FROM reviews
                    GROUP BY persona
                """)
            
            stats['persona_distribution'] = {
                row['persona']: row['count'] 
                for row in self.cursor.fetchall()
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def log_event(self, user_id: str, event_type: str, event_data: Dict = None):
        """Log analytics event"""
        try:
            self.cursor.execute("""
                INSERT INTO analytics (user_id, event_type, event_data)
                VALUES (?, ?, ?)
            """, (
                user_id,
                event_type,
                json.dumps(event_data) if event_data else None
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Error logging event: {e}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Singleton instance
_db_instance = None

def get_db() -> DatabaseManager:
    """Get database instance (singleton)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance
