import pandas as pd


def bronze():
    df = pd.read_csv("telecom_customer_churn.csv")
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    # df["ingestion_date"] = pd.Timestamp.now()
    df.to_csv("bronze.csv", index=False)
    return df


if __name__ == "__main__":
    bronze()
