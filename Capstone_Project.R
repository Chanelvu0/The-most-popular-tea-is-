#### Setup ####
options(scipen = 10)

dir = "/Users/chanelvu/Desktop/"
file = "cleaned_tea_reviews.csv"
path = paste0(dir, file)

tea_df = read.csv(path, stringsAsFactors = FALSE)

tea_df[ , "HelpfulnessNumeric"] = as.numeric(gsub("%", "", tea_df[ , "HelpfulnessScore"]))
tea_df[ , "ReviewLength"] = nchar(tea_df[ , "Text"])
tea_df[ , "ReviewDate"] = as.Date(tea_df[ , "ReviewDate"])

#### Score variance by tea group ####
score_var = aggregate(tea_df[ , "Score"], by = list(tea_df[ , "TeaGroup"]), FUN = var)
colnames(score_var) = c("TeaGroup", "ScoreVariance")
print(score_var)
#I looked at the score variance for each tea group to see how much people agreed 
#or disagreed in their reviews. Spiced Tea had the most mixed opinions, with the 
#highest variance at 1.64. Herbal Tea was the most consistent, with the lowest variance 
#at 1.22. The other teas — Black, Green, Oolong, and White — all had similar variances 
#between 1.25 and 1.44, which shows there was some variety in feedback, but nothing extreme.

#### Avg helpfulness by tea group ####
help_avg = aggregate(tea_df[ , "HelpfulnessNumeric"], by = list(tea_df[ , "TeaGroup"]), FUN = mean, na.rm = TRUE)
colnames(help_avg) = c("TeaGroup", "AvgHelpfulness")
print(help_avg)

#I also checked the average helpfulness of reviews for each tea group. Oolong had the highest at around 83.9%,
#meaning people found those reviews the most useful. Herbal and White Tea were also rated highly. On the lower 
#end, Spiced Tea had the lowest average helpfulness at 76.3%, which might mean those reviews weren’t as clear or 
#detailed. The rest — Black and Green Tea — were somewhere in the middle.

#### Sentiment count and proportion ####
tea_df[ , "Sentiment"] = ifelse(tea_df[ , "Score"] >= 4, "Positive",
                                ifelse(tea_df[ , "Score"] == 3, "Neutral", "Negative"))
sent_table = table(tea_df[ , "TeaGroup"], tea_df[ , "Sentiment"])
print(sent_table)

sent_prop = prop.table(sent_table, margin = 1)
print(round(sent_prop, 3))

#I looked at the sentiment of reviews across each tea group, 
#splitting them into positive, neutral, and negative. Most reviews 
#overall were positive, but the breakdown varied a bit by group. Herbal Tea 
#had the highest percentage of positive reviews (around 85%), while Spiced 
#Tea had the lowest at about 79%, along with the highest share of negative 
#feedback (14%). Green and Black Tea also had a slightly higher portion of 
#negative reviews compared to others. So while all groups were mostly reviewed 
#positively, some had more mixed feelings than others.



# Round to month
tea_df[ , "ReviewMonth"] = format(tea_df[ , "ReviewDate"], "%Y-%m")

# Count reviews per month
review_counts = table(tea_df[ , "ReviewMonth"])
review_months = as.Date(paste0(names(review_counts), "-01"))

# Plot
plot(review_months, as.numeric(review_counts),
     type = "l",
     col = "darkgreen",
     lwd = 2,
     main = "Review Trend Over Time",
     xlab = "Date",
     ylab = "Number of Reviews")

#Tracking review trends helps spot when interest in tea products was
#growing or slowing. A steady rise may suggest stronger demand or more 
#customers entering the market, while drops may show seasonality or changes
#in product availability.

top_products = sort(table(tea_df[ , "ProductId"]), decreasing = TRUE)[1:10]
print(top_products)
top_ids = names(top_products)
subset = tea_df[tea_df[ , "ProductId"] %in% top_ids, ]
aggregate(subset[ , "Score"], by = list(subset[ , "ProductId"]), FUN = mean)

#These are the top 10 tea products with the most reviews. 
#Most of them have strong average scores, around 4.37 to 4.49, which 
#shows customers generally like them. A few, like product B0061IUIDY, 
#still made the top list but have slightly lower ratings, which might be worth 
#investigating further.
#Helps businesses prioritize what to promote or improve, Shows customer favorites