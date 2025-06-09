# %%
def clean_noaa_rainfall(filepath):
    df = pd.read_csv(filepath)
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df["PRECIP_MM"] = df["AA1"].str.split(",", expand=True)[1]
    df["PRECIP_MM"] = pd.to_numeric(df["PRECIP_MM"], errors="coerce")
    
    df = df[(df["PRECIP_MM"] >= 0) & (df["PRECIP_MM"] < 500)]  # max ~50mm (2 inches) per hour

    df["PRECIP_IN"] = df["PRECIP_MM"] / 10 * 0.0393701
    df["DATE_HOUR"] = df["DATE"].dt.floor("h")  # lowercase 'h' to avoid warning
    return df[["STATION", "DATE_HOUR", "PRECIP_IN"]]



# %%
import pandas as pd

def clean_noaa_rainfall(filepath):
    df = pd.read_csv(filepath)

    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

    df["PRECIP_MM"] = df["AA1"].str.split(",", expand=True)[1]
    df["PRECIP_MM"] = pd.to_numeric(df["PRECIP_MM"], errors="coerce")

    df["PRECIP_IN"] = df["PRECIP_MM"] / 10 * 0.0393701

    df["DATE_HOUR"] = df["DATE"].dt.floor("h")

    return df[["STATION", "DATE_HOUR", "PRECIP_IN"]]

# %%
df_tucson = clean_noaa_rainfall("/Users/elliecapra/Downloads/AAE 718/Tucson International Airport.csv")
df_douglas = clean_noaa_rainfall("/Users/elliecapra/Downloads/AAE 718/Douglas Bisbee International Airport .csv")
df_nogales = clean_noaa_rainfall("/Users/elliecapra/Downloads/AAE 718/Nogales International Airport – KOLS.csv")
df_safford = clean_noaa_rainfall("/Users/elliecapra/Downloads/AAE 718/Safford Municipal Airport.csv")

# %%
# drop the NaN values for Tucson in "PRECIP_IN" column
df_tucson = df_tucson.dropna(subset=["PRECIP_IN"])

df_tucson = df_tucson.reset_index(drop=True)
df_tucson.head()

# %%
# drop the NaN values for Tucson in "PRECIP_IN" column
df_douglas = df_douglas.dropna(subset=["PRECIP_IN"])

df_douglas = df_douglas.reset_index(drop=True)
df_douglas.head()

# %%
# drop the NaN values for nogales in "PRECIP_IN" column
df_nogales = df_nogales.dropna(subset=["PRECIP_IN"])

df_nogales = df_nogales.reset_index(drop=True)
df_nogales.head()

# %%
# drop the NaN values for nogales in "PRECIP_IN" column
df_safford = df_safford.dropna(subset=["PRECIP_IN"])

df_safford = df_safford.reset_index(drop=True)
df_safford.head()

# %%
df_tucson["STATION_NAME"] = "Tucson"
df_douglas["STATION_NAME"] = "Douglas"
df_nogales["STATION_NAME"] = "Nogales"
df_safford["STATION_NAME"] = "Safford"

# %%
df_all = pd.concat([df_tucson, df_douglas, df_nogales, df_safford], ignore_index=True)

df_all["DATE_ONLY"] = df_all["DATE_HOUR"].dt.date
df_all["YEAR"] = df_all["DATE_HOUR"].dt.year

# %%
daily_rain = df_all.groupby(["STATION_NAME", "DATE_ONLY"]).agg({
    "PRECIP_IN": "sum"
}).reset_index()

# %%

daily_rain["YEAR"] = pd.to_datetime(daily_rain["DATE_ONLY"]).dt.year

daily_rain["HEAVY_RAIN"] = daily_rain["PRECIP_IN"] > 1.0

heavy_rain_summary = daily_rain.groupby(["STATION_NAME", "YEAR"]).agg({
    "HEAVY_RAIN": "sum"
}).reset_index()


# %%

df_all["DATE_ONLY"] = df_all["DATE_HOUR"].dt.date
df_all["YEAR"] = df_all["DATE_HOUR"].dt.year

print("Years before filter:", df_all["YEAR"].unique())

df_all = df_all[df_all["YEAR"] != 2005]

print("Years after filter:", df_all["YEAR"].unique())

daily_rain = df_all.groupby(["STATION_NAME", "DATE_ONLY"])["PRECIP_IN"].sum().reset_index()
daily_rain["YEAR"] = pd.to_datetime(daily_rain["DATE_ONLY"]).dt.year

annual_total = df_all.groupby(["STATION_NAME", "YEAR"])["PRECIP_IN"].sum().reset_index()

print(annual_total.sort_values("PRECIP_IN", ascending=False).head())

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

sns.lineplot(data=heavy_rain_summary, x="YEAR", y="HEAVY_RAIN", hue="STATION_NAME")
plt.title("Heavy Rain Days per Year")
plt.xlabel("Year")
plt.ylabel("Days > 1 inch Rain")
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.show()


# %%
annual_total = df_all.groupby(["STATION_NAME", "YEAR"])["PRECIP_IN"].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=annual_total, x="YEAR", y="PRECIP_IN", hue="STATION_NAME")
plt.title("Total Annual Rainfall by Station")
plt.ylabel("Total Rainfall (inches)")
plt.xlabel("Year")
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.show()

# %%
df_all["MONTH"] = df_all["DATE_HOUR"].dt.month
monsoon_df = df_all[df_all["MONTH"].isin([7, 8, 9])]

monsoon_total = monsoon_df.groupby(["STATION_NAME", "YEAR"])["PRECIP_IN"].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=monsoon_total, x="YEAR", y="PRECIP_IN", hue="STATION_NAME")
plt.title("Monsoon Season Rainfall (July–Sept) by Year")
plt.ylabel("Rainfall (inches)")
plt.xlabel("Year")
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.show()


# %%
daily_rain = df_all.groupby(["STATION_NAME", "DATE_ONLY"])["PRECIP_IN"].sum().reset_index()
daily_rain["YEAR"] = pd.to_datetime(daily_rain["DATE_ONLY"]).dt.year

daily_max = daily_rain.groupby(["STATION_NAME", "YEAR"])["PRECIP_IN"].max().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=daily_max, x="YEAR", y="PRECIP_IN", hue="STATION_NAME")
plt.title("Max Daily Rainfall per Year by Station")
plt.ylabel("Maximum 1-Day Rainfall (inches)")
plt.xlabel("Year")
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.show()


# %%
df_all["MONTH"] = df_all["DATE_HOUR"].dt.month

monthly_rain = df_all.groupby(["STATION_NAME", "MONTH"])["PRECIP_IN"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_rain, x="MONTH", y="PRECIP_IN", hue="STATION_NAME", marker="o")
plt.title("Average Monthly Rainfall by Station")
plt.xlabel("Month")
plt.ylabel("Avg Rainfall (inches)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.show()


