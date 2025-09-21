"""
Content Scheduler for JACAI - Automated Posting
"""
import sqlite3
from datetime import datetime, timedelta
import asyncio
from typing import List, Dict
import json
from social_media_service import social_service
from ai_service import ai_service

class ContentScheduler:
    def __init__(self):
        self.init_scheduler_db()
    
    def init_scheduler_db(self):
        """Initialize scheduler database tables"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic TEXT NOT NULL,
                platforms TEXT NOT NULL,
                style TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending',
                content_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                posted_at TIMESTAMP,
                error_message TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automation_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                topic_template TEXT,
                platforms TEXT NOT NULL,
                style TEXT NOT NULL,
                frequency TEXT NOT NULL,
                time_slots TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def schedule_post(self, user_id: int, topic: str, platforms: List[str], style: str, scheduled_time: datetime) -> Dict:
        """Schedule a post for future publishing"""
        try:
            conn = sqlite3.connect('jacai.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scheduled_posts (user_id, topic, platforms, style, scheduled_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, topic, json.dumps(platforms), style, scheduled_time))
            
            post_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "post_id": post_id,
                "message": f"Post scheduled for {scheduled_time}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_automation_rule(self, user_id: int, name: str, topic_template: str, 
                             platforms: List[str], style: str, frequency: str, time_slots: List[str]) -> Dict:
        """Create automation rule for recurring posts"""
        try:
            conn = sqlite3.connect('jacai.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO automation_rules (user_id, name, topic_template, platforms, style, frequency, time_slots)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, name, topic_template, json.dumps(platforms), style, frequency, json.dumps(time_slots)))
            
            rule_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "rule_id": rule_id,
                "message": f"Automation rule '{name}' created"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_pending_posts(self) -> List[Dict]:
        """Get posts ready to be published"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, topic, platforms, style, scheduled_time, content_json
            FROM scheduled_posts 
            WHERE status = 'pending' AND scheduled_time <= ?
        ''', (datetime.now(),))
        
        posts = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": post[0],
                "user_id": post[1],
                "topic": post[2],
                "platforms": json.loads(post[3]),
                "style": post[4],
                "scheduled_time": post[5],
                "content": json.loads(post[6]) if post[6] else None
            }
            for post in posts
        ]
    
    def process_scheduled_posts(self):
        """Process all pending scheduled posts"""
        pending_posts = self.get_pending_posts()
        
        for post in pending_posts:
            try:
                # Generate content if not already generated
                if not post["content"]:
                    content_results = []
                    for platform in post["platforms"]:
                        content = ai_service.generate_content(post["topic"], platform, post["style"])
                        content_results.append({
                            "platform": platform,
                            "content": content
                        })
                    
                    # Save generated content
                    self.update_post_content(post["id"], content_results)
                    post["content"] = content_results
                
                # Post to social media platforms
                self.publish_post(post)
                
            except Exception as e:
                self.mark_post_failed(post["id"], str(e))
    
    def publish_post(self, post: Dict):
        """Publish post to social media platforms"""
        try:
            # Get user's social accounts
            user_accounts = self.get_user_social_accounts(post["user_id"])
            
            success_count = 0
            total_platforms = len(post["platforms"])
            
            for content_item in post["content"]:
                platform = content_item["platform"]
                content = content_item["content"]
                
                # Find matching social account
                account = next((acc for acc in user_accounts if acc["platform"] == platform), None)
                
                if account:
                    result = social_service.post_content(
                        platform, 
                        content, 
                        account["access_token"], 
                        account.get("account_id")
                    )
                    
                    if result["success"]:
                        success_count += 1
            
            if success_count > 0:
                self.mark_post_completed(post["id"], f"Posted to {success_count}/{total_platforms} platforms")
            else:
                self.mark_post_failed(post["id"], "No successful posts")
                
        except Exception as e:
            self.mark_post_failed(post["id"], str(e))
    
    def get_user_social_accounts(self, user_id: int) -> List[Dict]:
        """Get user's linked social accounts"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT platform, access_token, account_name
            FROM social_accounts 
            WHERE user_id = ? AND is_active = TRUE
        ''', (user_id,))
        
        accounts = cursor.fetchall()
        conn.close()
        
        return [
            {
                "platform": acc[0],
                "access_token": acc[1],
                "account_name": acc[2]
            }
            for acc in accounts
        ]
    
    def update_post_content(self, post_id: int, content: List[Dict]):
        """Update post with generated content"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scheduled_posts 
            SET content_json = ? 
            WHERE id = ?
        ''', (json.dumps(content), post_id))
        
        conn.commit()
        conn.close()
    
    def mark_post_completed(self, post_id: int, message: str):
        """Mark post as completed"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scheduled_posts 
            SET status = 'completed', posted_at = ?, error_message = ?
            WHERE id = ?
        ''', (datetime.now(), message, post_id))
        
        conn.commit()
        conn.close()
    
    def mark_post_failed(self, post_id: int, error: str):
        """Mark post as failed"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scheduled_posts 
            SET status = 'failed', error_message = ?
            WHERE id = ?
        ''', (error, post_id))
        
        conn.commit()
        conn.close()
    
    def get_user_scheduled_posts(self, user_id: int) -> List[Dict]:
        """Get user's scheduled posts"""
        conn = sqlite3.connect('jacai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, topic, platforms, style, scheduled_time, status, error_message
            FROM scheduled_posts 
            WHERE user_id = ?
            ORDER BY scheduled_time DESC
            LIMIT 50
        ''', (user_id,))
        
        posts = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": post[0],
                "topic": post[1],
                "platforms": json.loads(post[2]),
                "style": post[3],
                "scheduled_time": post[4],
                "status": post[5],
                "error_message": post[6]
            }
            for post in posts
        ]

# Global scheduler instance
scheduler = ContentScheduler()