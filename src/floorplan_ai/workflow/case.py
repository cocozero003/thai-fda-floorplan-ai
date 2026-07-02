"""Synthetic screening case objects for officer workflow simulations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from floorplan_ai.annotation.schema import FloorPlanAnnotation


class ScreeningCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    annotation: FloorPlanAnnotation
    officer_comment: str = ""
    officer_override: str = ""
    status: str = "officer_review_required"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    advisory_only: bool = True
    synthetic_data_only: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_annotation(cls, annotation: FloorPlanAnnotation, case_id: str | None = None) -> "ScreeningCase":
        return cls(
            case_id=case_id or f"case-{annotation.annotation_id}",
            annotation=annotation,
            metadata={
                "data_classification": "synthetic",
                "contains_real_thai_fda_data": False,
                "human_officer_responsible": True,
            },
        )

    def with_officer_input(self, comment: str, override: str) -> "ScreeningCase":
        updated = self.model_copy(deep=True)
        updated.officer_comment = comment
        updated.officer_override = override
        return updated
