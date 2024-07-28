import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

df = pd.read_csv("persona.csv")
df.head()
df.info()
df.shape

#####################
#VERIYI TANIMA
#####################

df["SOURCE"].nunique()
df["SOURCE"].value_counts()

df["PRICE"].nunique()

df["PRICE"].value_counts()

df["COUNTRY"].value_counts()

df.groupby("COUNTRY").agg({"PRICE": "sum"})

df.groupby("SOURCE").agg({"PRICE": "count"})

df.groupby("COUNTRY").agg({"PRICE": "mean"})

df.groupby("SOURCE").agg({"PRICE": "mean"})

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

##################
#COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
##################
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})

##################
#Çıktıyı PRICE’a göre sıralayınız.
##################
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)

agg_df.reset_index(inplace=True)

#################
#Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz
#################
agg_df["AGE"] = agg_df["AGE"].astype("category")
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, 70], labels=["0_18", "19_23", "24_30", "31_40", "41_70"])

################
#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
################
agg_df["customers_level_based"] = agg_df["COUNTRY"] + "_" + agg_df["SOURCE"] + "_" + agg_df["SEX"] + "_" + agg_df["AGE_CAT"].astype(str)
agg_df[["customers_level_based", "PRICE"]]
agg_df["customers_level_based"] = agg_df["customers_level_based"].str.upper()

###############
#Yeni müşterileri (personaları) segmentlere ayırınız.
###############
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4 , labels=["D", "C", "B", "A"])

#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız)
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]}).round(2)

##############
#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz
##############

#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

#35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user1 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user1]


