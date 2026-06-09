import pandas as pd
from bronze import bronze

def silver():

    df = bronze()

    df["offer"] = df["offer"].fillna("No offer")
    df["avg_monthly_long_distance_charges"] = df[
        "avg_monthly_long_distance_charges"
    ].fillna(0)

    df["multiple_lines"] = df["multiple_lines"].fillna("No Internet Service")
    df["internet_type"] = df["internet_type"].fillna("None")

    df["unlimited_data"] = df["unlimited_data"].fillna("No Internet Service")
    df["streaming_music"] = df["streaming_music"].fillna("No Internet Service")
    df["streaming_movies"] = df["streaming_movies"].fillna("No Internet Service")
    df["streaming_tv"] = df["streaming_tv"].fillna("No Internet Service")
    df["premium_tech_support"] = df["premium_tech_support"].fillna(
        "No Internet Service"
    )
    df["device_protection_plan"] = df["device_protection_plan"].fillna(
        "No Internet Service"
    )
    df["online_backup"] = df["online_backup"].fillna("No Internet Service")
    df["online_security"] = df["online_security"].fillna("No Internet Service")

    df["avg_monthly_gb_download"] = df["avg_monthly_gb_download"].fillna(0)

    df.loc[df["customer_status"].isin(["Stayed", "Joined"]), "churn_category"] = df[
        "churn_category"
    ].fillna("None")

    df["churn_reason"] = df["churn_reason"].fillna("None")

    df.loc[df["monthly_charge"] < 0, "monthly_charge"] = 0

    category_map = {
        # Competitor Offer
        "Competitor had better devices": "Competitor Offer",
        "Competitor made better offer": "Competitor Offer",
        "Competitor offered more data": "Competitor Offer",
        "Competitor offered higher download speeds": "Competitor Offer",
        # Price Issue
        "Price too high": "Price Issue",
        "Long distance charges": "Price Issue",
        "Extra data charges": "Price Issue",
        "Lack of affordable download/upload speed": "Price Issue",
        # Dissatisfaction
        "Attitude of support person": "Dissatisfaction",
        "Attitude of service provider": "Dissatisfaction",
        "Product dissatisfaction": "Dissatisfaction",
        "Network reliability": "Dissatisfaction",
        "Service dissatisfaction": "Dissatisfaction",
        "Poor expertise of online support": "Dissatisfaction",
        "Poor expertise of phone support": "Dissatisfaction",
        "Lack of self-service on Website": "Dissatisfaction",
        "Limited range of services": "Dissatisfaction",
        # Other
        "Don't know": "Other",
        "Moved": "Other",
        "Deceased": "Other",
        "None": "None",
    }

    df["churn_reason"] = df["churn_reason"].replace(category_map)

    df["zip_code"] = df["zip_code"].astype(str)

    df = df.drop_duplicates()

    df.to_csv("new_silver.csv", index=False)

    return df


if __name__ == "__main__":
    silver()
