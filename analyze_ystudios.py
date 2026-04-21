import pandas as pd
import os


def generate_client_report(csv_file_path, output_folder="client_deliverables"):

    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(csv_file_path)

    print("=" * 60)
    print("GENERATING CLIENT DELIVERABLES")
    print("=" * 60)

    print("\n1. BASIC DATA SUMMARY")
    print("-" * 40)
    print(f"Total records: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"File size: {os.path.getsize(csv_file_path) / 1024:.1f} KB")

    clean_file = f"{output_folder}/clean_data.csv"
    df.to_csv(clean_file, index=False)
    print(f"\nClean data saved: {clean_file}")

    excel_file = f"{output_folder}/complete_report.xlsx"
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Raw Data", index=False)

        summary = pd.DataFrame(
            {
                "Metric": ["Total Records", "Date Range", "Last Updated"],
                "Value": [len(df), "Current", pd.Timestamp.now().strftime("%Y-%m-%d")],
            }
        )
        summary.to_excel(writer, sheet_name="Summary", index=False)

        column_info = pd.DataFrame(
            {
                "Column Name": df.columns,
                "Data Type": df.dtypes.astype(str),
                "Non-Null Count": df.count().values,
                "Unique Values": df.nunique().values,
            }
        )
        column_info.to_excel(writer, sheet_name="Column Info", index=False)

    print(f"Excel report saved: {excel_file}")

    price_columns = [
        col for col in df.columns if "price" in col.lower() or "cost" in col.lower()
    ]
    if price_columns:
        price_col = price_columns[0]
        df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
        valid_prices = df[df[price_col] > 0][price_col]

        if len(valid_prices) > 0:
            print("\nPRICE STATISTICS")
            print("-" * 40)
            print(f"Average: {valid_prices.mean():.2f}")
            print(f"Minimum: {valid_prices.min():.2f}")
            print(f"Maximum: {valid_prices.max():.2f}")
            print(f"Median: {valid_prices.median():.2f}")

    status_columns = [
        col
        for col in df.columns
        if "status" in col.lower() or "available" in col.lower()
    ]
    if status_columns:
        status_col = status_columns[0]
        print("\nSTATUS BREAKDOWN")
        print("-" * 40)
        for status, count in df[status_col].value_counts().head(10).items():
            percentage = (count / len(df)) * 100
            print(f"{status}: {count} ({percentage:.1f}%)")

    print("\nTOP 10 LISTS")
    print("-" * 40)

    if price_columns:
        price_col = price_columns[0]
        top_expensive = df.nlargest(10, price_col)
        if len(top_expensive) > 0:
            print("\nMost Expensive Items:")
            for idx, row in top_expensive.head(5).iterrows():
                name_col = df.columns[0]
                print(f"   {row[name_col]}: {row[price_col]:.2f}")

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"\nFound {duplicates} duplicate rows")
        df_unique = df.drop_duplicates()
        unique_file = f"{output_folder}/unique_data.csv"
        df_unique.to_csv(unique_file, index=False)
        print(f"Unique data saved: {unique_file}")
    else:
        print(f"\nNo duplicate rows found")

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) > 0:
        print("\nMISSING VALUES")
        print("-" * 40)
        for col, count in missing_cols.items():
            percentage = (count / len(df)) * 100
            print(f"{col}: {count} missing ({percentage:.1f}%)")

    summary_file = f"{output_folder}/summary_report.txt"
    with open(summary_file, "w", encoding="utf-8") as file_handle:
        file_handle.write("DATA SCRAPING SUMMARY REPORT\n")
        file_handle.write("=" * 40 + "\n")
        file_handle.write(
            f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file_handle.write(f"Total records: {len(df)}\n")
        file_handle.write(f"Total columns: {len(df.columns)}\n")
        file_handle.write(f"Columns: {', '.join(df.columns)}\n")
        file_handle.write("\nFILES INCLUDED:\n")
        file_handle.write(f"  - clean_data.csv: All data in CSV format\n")
        file_handle.write(
            f"  - complete_report.xlsx: Excel report with multiple sheets\n"
        )
        file_handle.write(
            f"  - {os.path.basename(csv_file_path)}: Original scraped data\n"
        )

    print(f"\nText summary saved: {summary_file}")

    print("\n" + "=" * 60)
    print("FINAL DELIVERABLES READY")
    print("=" * 60)
    print(f"\nFolder: {output_folder}/")
    print(f"   clean_data.csv")
    print(f"   complete_report.xlsx")
    print(f"   summary_report.txt")
    if duplicates > 0:
        print(f"   unique_data.csv")
    print(f"   {os.path.basename(csv_file_path)}")

    print("\nReady to send to client")
    return output_folder


generate_client_report("data/ystudios_products_detailed.csv")
