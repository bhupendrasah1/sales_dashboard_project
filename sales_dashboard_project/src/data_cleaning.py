import pandas as pd


def clean_sales_data(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)


    df.columns = [c.strip() for c in df.columns]

    
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y", errors="coerce")

    
    df["Category"] = df["Category"].str.strip().str.title()
    df["Region"] = df["Region"].str.strip().str.title()


    before = len(df)
    df = df.drop_duplicates(subset=["Order ID"], keep="first")
    print(f"Removed {before - len(df)} duplicate rows.")


   
    df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
    df["Unit Price"] = df["Unit Price"].fillna(df["Unit Price"].median())
    df["Region"] = df["Region"].fillna("Unknown")

   
    df["Revenue"] = (df["Quantity"] * df["Unit Price"]).round(2)

    
    before = len(df)
    df = df.dropna(subset=["Order Date"])
    print(f"Dropped {before - len(df)} rows with invalid dates.")

    
    df = df.sort_values("Order Date").reset_index(drop=True)

    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path} ({len(df)} rows).")
    return df


if __name__ == "__main__":
    clean_sales_data("data/raw_sales_data.csv", "data/clean_sales_data.csv")
