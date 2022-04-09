from django.db import models


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # Abstract모델은 데이터베이스에 저장되지 않는다. 코드에서만 쓰기위해 정의하는 것임
