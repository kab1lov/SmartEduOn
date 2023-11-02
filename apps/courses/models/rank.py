from django.db.models import ForeignKey, CASCADE, PositiveIntegerField

from shared.drf.models import BaseModel


class Rating(BaseModel):
    speaker = ForeignKey('users.User', on_delete=CASCADE, related_name='ratings')
    value = PositiveIntegerField()

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)

        ratings = self.speaker.ratings.all()
        total_ratings = ratings.count()
        total_rating_value = sum([rating.value for rating in ratings])
        new_rating = total_rating_value / total_ratings if total_ratings > 0 else 0

        self.speaker.rating = round(new_rating, 2)
        self.speaker.save()


class RatingCourse(BaseModel):
    course = ForeignKey('courses.Course', on_delete=CASCADE, related_name='ratings')
    value = PositiveIntegerField()

    def save(self, *args, **kwargs):
        super(RatingCourse, self).save(*args, **kwargs)

        ratings = self.course.ratings.all()
        total_ratings = ratings.count()
        total_rating_value = sum([rating.value for rating in ratings])
        new_rating = total_rating_value / total_ratings if total_ratings > 0 else 0

        self.course.rating = round(new_rating, 2)
        self.course.save()
