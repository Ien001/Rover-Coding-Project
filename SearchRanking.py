import sys
import pandas as pd


def main():
	# read in reviews file
	reviews_file = sys.argv[1]
	df = pd.read_csv(reviews_file)

	"""
	 construct a dataframe to store the required data
	* Sitter email (`email`)
	* Sitter name (`name`)
	* Profile Score (`profile_score`)
	* Ratings Score (`ratings_score`)
	* Search Score (`search_score`)
	* the number of reviews of one sitter (`review_times`)
	""" 
	ret = pd.DataFrame(columns=['name','email','profile_score','ratings_score','search_score','review_times'])
	ret['name'] = df['sitter']
	ret['email'] = df['sitter_email']
	
	# calculate review times
	df_review_times = ret.groupby(['name']).count()['email']

	# remove the duplicated sitters
	ret = ret.groupby(['name','email']).sum()
	ret['review_times'] = list(df_review_times)
	
	# calculate profile score
	# using 5 times the fraction of the English alphabet comprised by the distinct letters in the sitter's name
	ret['profile_score'] = [5/len(set(x[0].lower().replace(" ","").replace(".",""))) for x in ret.index]

	# calculate ratings score
	# using the average of their stay ratings.
	ret['ratings_score'] = list(df.groupby(['sitter']).sum()['rating'] / df_review_times)

	# calculate search score
	# using the weighted average of the Profile Score and Ratings
	ret['search_score'] = (ret['profile_score'] + ret['ratings_score'])/2

	# When a sitter has 10 or more stays, their Search Score is equal to the Ratings Score
	ret.loc[ret['review_times']>10,'search_score'] = ret.loc[ret['review_times']>10,'ratings_score']

	# round to two decimal
	ret = ret.round(2)

	# remove the 'review_times' column 
	ret = ret.drop(['review_times'], axis=1)

	# add 'sitter_name' column for sorting
	ret['sitter_name'] = [x[0] for x in ret.index]
	# sort according to 'search_score' and 'sitter_name'
	ret = ret.sort_values(['search_score', 'sitter_name'],ascending = (False,True))
	# remove 'sitter_name' column
	ret = ret.drop(['sitter_name'], axis=1)

	# save the result
	ret.to_csv('sitters.csv')

if __name__ == '__main__':
	main()