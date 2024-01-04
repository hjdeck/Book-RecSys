import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:

    books = pd.read_csv('./data/Books.csv', low_memory = False)
    ratings = pd.read_csv('./data/Ratings.csv')
    users = pd.read_csv('./data/Users.csv')
    book_ratings = ratings.merge(books, on = 'ISBN')

    def getRatings(self):
        
        # Users that gave >200 ratings
        reviewers = self.book_ratings.groupby('User-ID').count()['Book-Rating']>200
        reviewers_index = reviewers[reviewers].index
        reviewers_df = self.book_ratings[self.book_ratings['User-ID'].isin(reviewers_index)]
        # Books with >=50 ratings
        rated_books = reviewers_df.groupby('Book-Title').count()['Book-Rating']>=50
        rated_books_index = rated_books[rated_books].index
        # Ratings with >=50 ratings only from users who gave >200 ratings
        ratings = reviewers_df[reviewers_df['Book-Title'].isin(rated_books_index)]
        return ratings

    def getSimilarity(self):
        ratings = self.getRatings()
        pt = ratings.pivot_table(index = 'Book-Title', columns = 'User-ID', values = 'Book-Rating')
        pt.fillna(0, inplace = True)
        similarity_score = cosine_similarity(pt)
        return pt, similarity_score

    def recommend(self, book_name):
        pt, similarity_score = self.getSimilarity()
        index = np.where(pt.index == book_name)[0][0]
        similar = sorted(enumerate(similarity_score[index]), key = lambda x:x[1], reverse = True)[1:11]
        rec_books = []
        for i in similar:
            item = []
            temp = self.books[self.books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
            rec_books.append(item)
        return rec_books
    
    def getPopular(self):
        num_ratings = self.book_ratings.groupby('Book-Title').count()['Book-Rating'].reset_index()
        num_ratings.rename(columns = {'Book-Rating':'num_ratings'}, inplace = True)

        avg_ratings = self.book_ratings.groupby('Book-Title').mean(numeric_only = True)['Book-Rating'].reset_index()
        avg_ratings.rename(columns = {'Book-Rating':'avg_ratings'}, inplace = True)

        pop = num_ratings.merge(avg_ratings, on = 'Book-Title')
        popular = pop[pop['num_ratings'] >= 300].sort_values('avg_ratings', ascending = False)
        popular_df = popular.merge(self.books, on = 'Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-M','num_ratings','avg_ratings']]
        return popular_df[0:10].values.tolist()


    
def main():
    recommender = Recommender()
    popular = recommender.getPopular()
    print(popular[0])

if __name__ == "__main__":
    main()