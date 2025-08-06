import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from models.course import Course, CourseCategory, CourseLevel, CourseStatus
from sqlalchemy.orm import Session


class CourseService:
    """Service for managing courses and educational content"""

    def __init__(self, db: Session):
        self.db = db

    def create_course(self, course_data: Dict[str, Any]) -> Course:
        """Create a new course"""
        course = Course(
            title=course_data["title"],
            description=course_data["description"],
            category=course_data["category"],
            level=course_data["level"],
            duration_hours=course_data.get("duration_hours", 0),
            price=course_data.get("price", 0.0),
            instructor_id=course_data["instructor_id"],
            content_url=course_data.get("content_url"),
            thumbnail_url=course_data.get("thumbnail_url"),
            prerequisites=course_data.get("prerequisites", []),
            learning_objectives=course_data.get("learning_objectives", []),
            status=CourseStatus.DRAFT
        )

        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_course(self, course_id: int) -> Optional[Course]:
        """Get course by ID"""
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_courses(self,
                   category: Optional[CourseCategory] = None,
                   level: Optional[CourseLevel] = None,
                   status: Optional[CourseStatus] = None,
                   limit: int = 50,
                   offset: int = 0) -> List[Course]:
        """Get courses with filters"""
        query = self.db.query(Course)

        if category:
            query = query.filter(Course.category == category)
        if level:
            query = query.filter(Course.level == level)
        if status:
            query = query.filter(Course.status == status)

        return query.offset(offset).limit(limit).all()

    def update_course(self, course_id: int, update_data: Dict[str, Any]) -> Optional[Course]:
        """Update course information"""
        course = self.get_course(course_id)
        if not course:
            return None

        # Update fields
        for field, value in update_data.items():
            if hasattr(course, field) and value is not None:
                setattr(course, field, value)

        course.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(course)
        return course

    def publish_course(self, course_id: int) -> Dict[str, Any]:
        """Publish a course"""
        course = self.get_course(course_id)
        if not course:
            return {"error": "Course not found"}

        try:
            # Validate course before publishing
            if not self._validate_course_for_publishing(course):
                return {"error": "Course validation failed. Please complete all required fields."}

            course.status = CourseStatus.PUBLISHED
            course.published_at = datetime.utcnow()
            course.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "course_id": course.id,
                "status": "published",
                "published_at": course.published_at.isoformat()
            }

        except Exception as e:
            return {"error": f"Publishing failed: {str(e)}"}

    def _validate_course_for_publishing(self, course: Course) -> bool:
        """Validate course before publishing"""
        required_fields = [
            "title", "description", "category", "level", "instructor_id"
        ]

        for field in required_fields:
            if not getattr(course, field):
                return False

        return True

    def delete_course(self, course_id: int) -> bool:
        """Delete a course"""
        course = self.get_course(course_id)
        if not course:
            return False

        self.db.delete(course)
        self.db.commit()
        return True

    def get_course_statistics(self, course_id: Optional[int] = None) -> Dict[str, Any]:
        """Get course statistics"""
        query = self.db.query(Course)

        if course_id:
            query = query.filter(Course.id == course_id)

        total_courses = query.count()
        draft_courses = query.filter(Course.status == CourseStatus.DRAFT).count()
        published_courses = query.filter(Course.status == CourseStatus.PUBLISHED).count()
        archived_courses = query.filter(Course.status == CourseStatus.ARCHIVED).count()

        return {
            "total": total_courses,
            "draft": draft_courses,
            "published": published_courses,
            "archived": archived_courses
        }

    def search_courses(self, search_term: str, limit: int = 20) -> List[Course]:
        """Search courses by title or description"""
        return self.db.query(Course).filter(
            Course.title.ilike(f"%{search_term}%") |
            Course.description.ilike(f"%{search_term}%")
        ).limit(limit).all()

    def get_courses_by_instructor(self, instructor_id: int) -> List[Course]:
        """Get all courses by an instructor"""
        return self.db.query(Course).filter(Course.instructor_id == instructor_id).all()

    def archive_course(self, course_id: int) -> Dict[str, Any]:
        """Archive a course"""
        course = self.get_course(course_id)
        if not course:
            return {"error": "Course not found"}

        try:
            course.status = CourseStatus.ARCHIVED
            course.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "course_id": course.id,
                "status": "archived"
            }

        except Exception as e:
            return {"error": f"Archiving failed: {str(e)}"}
