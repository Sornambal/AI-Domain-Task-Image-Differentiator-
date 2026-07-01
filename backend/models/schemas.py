from typing import List, Optional

from pydantic import BaseModel


class RegionSchema(BaseModel):
    bbox: List[int]
    area_px: int
    centroid: List[int]
    location: str
    type: str


class StatisticsSchema(BaseModel):
    num_changed_regions: int
    percent_area_changed: float
    regions: List[RegionSchema]


class CompareResponse(BaseModel):
    original_a_url: str
    original_b_url: str
    diff_visualization_url: str
    heatmap_url: str
    statistics: StatisticsSchema
    ai_summary: str
