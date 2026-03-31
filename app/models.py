# app/models.py
from datetime import datetime, timezone
from typing import List, Dict, Optional

class TaskManager:
    """Handles all task data operations"""
    
    def __init__(self):
        self._tasks: List[Dict] = []
        self._next_id: int = 1
    
    def reset(self) -> None:
        """Clear all data - useful for testing"""
        self._tasks.clear()
        self._next_id = 1
    
    def create(self, title: str) -> Dict:
        """Create a new task"""
        task = {
            'id': self._next_id,
            'title': title,
            'completed': False,
            # 'created_at': datetime.utcnow().isoformat()
            'created_at': datetime.now(timezone.utc)
        }
        self._next_id += 1
        self._tasks.append(task)
        return task
    
    def get_all(self) -> List[Dict]:
        """Get all tasks"""
        return self._tasks.copy()
    
    def get_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a task by ID"""
        return next((t for t in self._tasks if t['id'] == task_id), None)
    
    def update(self, task_id: int, updates: Dict) -> Optional[Dict]:
        """Update a task"""
        task = self.get_by_id(task_id)
        if task:
            task.update(updates)
        return task
    
    def delete(self, task_id: int) -> bool:
        """Delete a task"""
        task = self.get_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False
    
    @property
    def count(self) -> int:
        """Return number of tasks"""
        return len(self._tasks)
