# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    TODO: Tạo expectation suite cho anonymized patient data.
    """
    context = gx.get_context()
    suite = gx.ExpectationSuite(name="patient_data_suite")

    # Lấy validator
    df = pd.read_csv("data/raw/patients_raw.csv", dtype={"cccd": str, "so_dien_thoai": str})
    batch = context.data_sources.pandas_default.read_dataframe(df)
    validator = context.get_validator(batch=batch, expectation_suite=suite)

    # --- TASK: Thêm các expectations ---

    # 1. patient_id không được null
    validator.expect_column_values_to_not_be_null("patient_id")

    # 2. TODO: cccd phải có đúng 12 ký tự
    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )

    # 3. TODO: ket_qua_xet_nghiem phải trong khoảng [0, 50]
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0.0,
        max_value=50.0
    )

    # 4. TODO: benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )

    # 5. TODO: email phải match regex pattern
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"    # TODO: email regex
    )

    # 6. TODO: Không được có duplicate patient_id
    validator.expect_column_values_to_be_unique(column="patient_id")

    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    """
    TODO: Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    raw_df = pd.read_csv("data/raw/patients_raw.csv")
    
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    # Check 1: Không còn CCCD gốc dạng số thuần túy
    # (sau anonymization, cccd phải là fake hoặc masked)
    original_cccds = set(raw_df["cccd"].astype(str).tolist())
    anon_cccds = set(df["cccd"].astype(str).tolist())
    overlapping_cccd = original_cccds.intersection(anon_cccds)
    if len(overlapping_cccd) > 0:
        results["success"] = False
        results["failed_checks"].append("Check 1: Found raw CCCDs in anonymized data")

    # Check 2: Không có null values trong các cột quan trọng
    important_cols = ["patient_id", "ho_ten", "cccd", "so_dien_thoai", "email", "benh"]
    for col in important_cols:
        if col in df.columns:
            if df[col].isnull().any():
                results["success"] = False
                results["failed_checks"].append(f"Check 2: Null values found in column '{col}'")

    # Check 3: Số rows phải bằng original
    if len(df) != len(raw_df):
        results["success"] = False
        results["failed_checks"].append("Check 3: Row count does not match original data")

    return results
