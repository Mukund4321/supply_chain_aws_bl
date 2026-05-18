import pandas as pd

# load_data reads the raw CSV file from disk and returns a DataFrame
# It also prints the shape so we immediately know if the file loaded correctly
def load_data(filepath: str) -> pd.DataFrame:
    # pd.read_csv parses each row into a column-aligned table (DataFrame)
    # Without this, we'd have to manually split every line by comma
    df = pd.read_csv(filepath)

    # Printing shape = (rows, columns) helps confirm we loaded all expected data
    # If rows are missing, the CSV might be truncated or have encoding issues
    print(f"[data_loader] Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")

    return df
