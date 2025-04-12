from sqlalchemy.orm import relationship

from models.domain.job import Job
from models.domain.response import Response

Job.responses = relationship(
    "Response", back_populates="job", cascade="all, delete-orphan"
)

Response.job = relationship("Job", back_populates="responses")
