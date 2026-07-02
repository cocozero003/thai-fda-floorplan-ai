from pathlib import Path

from PIL import Image

from floorplan_ai.annotation.schema import FloorPlanAnnotation
from floorplan_ai.features.spatial_features import extract_spatial_features
from floorplan_ai.heatmap.generator import generate_heatmap
from floorplan_ai.rules.rule_engine import evaluate_rules, load_rules


SAMPLE = Path("data/sample_synthetic/annotation_simple_factory.json")
RULES = Path("configs/rules_gmp_thai_fda.yaml")


def test_generate_heatmap_creates_png(tmp_path: Path) -> None:
    annotation = FloorPlanAnnotation.model_validate_json(SAMPLE.read_text(encoding="utf-8"))
    features = extract_spatial_features(annotation)
    findings = evaluate_rules(annotation, load_rules(RULES), features)
    output = tmp_path / "heatmap.png"

    result = generate_heatmap(annotation, findings, output_path=output)

    assert result == output
    assert output.exists()
    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == (annotation.image_width, annotation.image_height)
