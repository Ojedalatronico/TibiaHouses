# %%

import pandas as pd

df = pd.read_csv("houses.csv")
# %%
df


# %%
df.describe()

# %%
df[df.status != "auctioned (no bid yet)"]

# %%
df.status.iloc[0]
